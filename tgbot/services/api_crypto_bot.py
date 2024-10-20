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
            requests_currencies = await session.get(f"{self.base_url}/getExchangeRates")
            response_currencies = await requests_currencies.json()
            await session.close()

            currencies = response_currencies['result']
            rate = currencies[0]['rate']
            amount_crypto = amount / float(rate)

        async with aiohttp.ClientSession(headers={"Crypto-Pay-API-Token": self.token}, timeout=self.timeout) as session:
            data = {"amount": amount_crypto, "asset": 'USDT'}
            request = await session.post(f'{self.base_url}/createinvoice', data=data)
            await session.close()

            response = await request.json()

            return response['result']['pay_url']

    async def get_pay_status(self, bill_id):
        async with aiohttp.ClientSession(headers={"Crypto-Pay-API-Token": self.token}, timeout=self.timeout) as session:
            data = {
                "invoice_ids": bill_id,
                "count": 1
            }

            resp = await session.get(f"{self.base_url}/getInvoices", data=data)
            await session.close()
            r = await resp.json()
            if r['result']['items'][0]['status'] == "paid":
                return True
            return False


API_Crypto = CryptoBotAPI(api_token=settings.CRYPTO_BOT_API_TOKEN)
