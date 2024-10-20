# Импорт необходимых модулей.
import time

import random

import aiohttp

import hashlib

import secrets

from ..bot_settings import settings


# Класс работы с API платежной системой AAIO.
class AaioAPI:
    def __init__(self, aaio_api_key, aaio_id_shop, aaio_secret_key) -> None:
        self.api_key = aaio_api_key
        self.shop_id = aaio_id_shop
        self.secret_key = aaio_secret_key
        self.timeout = aiohttp.ClientTimeout(total=360)
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": self.api_key
        }

    async def generate_pay_link(self, amount: float) -> str:
        """
        Создает платежную ссылку для пополнения баланса.

        :param amount: Сумма пополнения баланса в профиле.
        :return: Платежная ссылка.
        """
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            order_id = f'{time.time()}_{secrets.token_hex(random.randint(5, 10))}'
            sign = f':'.join([str(self.shop_id), str(amount), 'RUB', str(self.secret_key), order_id])

            sign = hashlib.sha256(sign.encode('utf-8')).hexdigest(),

            params = {
                'merchant_id': self.shop_id, "amount": amount, "order_id": order_id, 'sign': sign, 'currency': 'RUB'
            }

            response = await session.post(url="https://aaio.io/merchant/pay", data=params)

            await session.close()

            return str(response.url)

    async def get_pay_status(self, order_id):
        async with aiohttp.ClientSession(headers=self.headers, timeout=self.timeout) as session:
            params = {'order_id': order_id, 'merchant_id': self.shop_id}
            response = await session.post(url="https://aaio.io/api/info-pay", data=params)

            await session.close()
            resp = await response.json()

            if resp['type'] == "success":
                if resp['status'] == "success" or resp['status'] == 'hold':
                    return True
                else:
                    return False
            else:
                return False


# Создание объекта класса Aaio для полноценной работы.
API_AAIO = AaioAPI(
    aaio_secret_key=settings.AAIO_SECRET_KEY,
    aaio_id_shop=settings.AAIO_ID_SHOP,
    aaio_api_key=settings.AAIO_API_KEY
)
