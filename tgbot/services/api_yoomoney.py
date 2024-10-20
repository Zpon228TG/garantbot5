import json

from aiohttp import ClientConnectorCertificateError

from ..bot_settings import settings, ARS
from tgbot.utils.const_functions import gen_id


class YoomoneyAPI:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token
        self.base_url = 'https://yoomoney.ru/api/'
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.arSession = ARS

    # Информация об аккаунте
    async def account_info(self):
        status, response = await self._request("account-info")

        return response['account']

    # Создание платежа
    async def generate_pay_link(self, pay_amount: float) -> tuple[str, int]:
        session = await self.arSession.get_session()

        bill_receipt = gen_id()

        get_wallet = await self.account_info()
        url = "https://yoomoney.ru/quickpay/confirm.xml?"

        pay_amount_bill = pay_amount + (pay_amount * 0.031)

        if float(pay_amount_bill) < 2:
            pay_amount_bill = 2.04

        payload = {
            'receiver': get_wallet,
            'quickpay_form': "button",
            'targets': 'Добровольное пожертвование',
            'paymentType': 'SB',
            'sum': pay_amount_bill,
            'label': bill_receipt,
        }

        for value in payload:
            url += str(value).replace("_", "-") + "=" + str(payload[value])
            url += "&"

        bill_link = str((await session.post(url[:-1].replace(" ", "%20"))).url)

        return bill_link, bill_receipt

    # Проверка платежа
    async def get_pay_status(self, receipt: str | int = None, records: int = 1) -> tuple[int, float]:
        data = {'type': 'deposition', 'details': 'true'}

        if receipt is not None:
            data['label'] = receipt
        if records is not None:
            data['records'] = records

        status, response = await self._request("operation-history", data)

        pay_status = 1
        pay_amount = None

        if status:
            pay_status = 2

            if len(response['operations']) >= 1:
                pay_currency = response['operations'][0]['amount_currency']
                pay_amount = response['operations'][0]['amount']

                pay_status = 3

                if pay_currency == "RUB":
                    pay_status = 0

        return pay_status, pay_amount

    # Запрос
    async def _request(self, method: str, data: dict = None) -> tuple[bool, any]:
        session = await self.arSession.get_session()

        url = self.base_url + method

        try:
            response = await session.post(url, headers=self.headers, data=data)
            response_data = json.loads((await response.read()).decode())

            if response.status == 200:
                return True, response_data
            else:

                return False, response_data
        except ClientConnectorCertificateError:
            return False, "CERTIFICATE_VERIFY_FAILED"

        except Exception as e:
            return False, str(e)


API_Yoomoney = YoomoneyAPI(api_token=settings.YOOMONEY_API_TOKEN.get_secret_value())
