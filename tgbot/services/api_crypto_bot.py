import aiohttp
from ..bot_settings import settings

class CryptoBotAPI:
    def __init__(self, api_token: str):
        self.token = api_token
        self.base_url = "https://pay.crypt.bot/api"
        self.timeout = aiohttp.ClientTimeout(total=360)

    async def generate_pay_link(self, amount: float) -> str:
        """
        Создает платежную ссылку для пополнения баланса.

        :param amount: Сумма пополнения баланса в профиле.
        :return: Платежная ссылка.
        """
        async with aiohttp.ClientSession(headers={"Crypto-Pay-API-Token": self.token}, timeout=self.timeout) as session:
            # Получаем курсы валют
            requests_currencies = await session.get(f"{self.base_url}/getExchangeRates")
            response_currencies = await requests_currencies.json()

            # Проверяем успешность запроса
            if not response_currencies.get('result'):
                raise Exception("Failed to fetch exchange rates")

            currencies = response_currencies['result']
            rate = currencies[0]['rate']  # Предполагается, что первый элемент - это нужная валюта
            amount_crypto = amount / float(rate)  # Конвертация суммы в криптовалюту

            # Создаем платежную ссылку
            data = {"amount": amount_crypto, "asset": 'USDT'}
            request = await session.post(f'{self.base_url}/createinvoice', json=data)  # Используем json вместо data
            response = await request.json()

            if response.get('result'):
                return response['result']['pay_url']
            else:
                raise Exception("Failed to create payment link: " + response.get('message', 'Unknown error'))

    async def get_pay_status(self, bill_id: str) -> bool:
        """
        Получает статус платежа по bill_id.

        :param bill_id: ID счета.
        :return: True, если счет оплачен, иначе False.
        """
        async with aiohttp.ClientSession(headers={"Crypto-Pay-API-Token": self.token}, timeout=self.timeout) as session:
            data = {
                "invoice_ids": [bill_id],  # Убедитесь, что это список
                "count": 1
            }

            resp = await session.post(f"{self.base_url}/getInvoices", json=data)  # Используем json вместо data
            r = await resp.json()

            if r.get('result') and r['result']['items']:
                return r['result']['items'][0]['status'] == "paid"
            return False  # Если результат не найден или items пуст, возвращаем False

# Создание экземпляра API Crypto
API_Crypto = CryptoBotAPI(api_token=settings.CRYPTO_BOT_API_TOKEN.get_secret_value())
