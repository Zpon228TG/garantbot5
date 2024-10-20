import time
import random
import aiohttp
import hashlib
import secrets

class AaioAPI:
    def __init__(self, aaio_api_key: str, aaio_id_shop: int, aaio_secret_key: str) -> None:
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
            # Формирование строки для подписи
            sign_string = f'{self.shop_id}:{amount}:RUB:{self.secret_key}:{order_id}'
            sign = hashlib.sha256(sign_string.encode('utf-8')).hexdigest()  # Генерация SHA256 подписи

            params = {
                'merchant_id': self.shop_id,
                "amount": amount,
                "order_id": order_id,
                'sign': sign,
                'currency': 'RUB'
            }

            response = await session.post(url="https://aaio.io/merchant/pay", data=params)
            response.raise_for_status()  # Проверка на наличие ошибок
            response_data = await response.json()  # Получаем ответ в формате JSON

            if response_data.get('success'):  # Проверка успешности ответа
                return response_data.get('pay_url')  # Возвращаем платежную ссылку
            else:
                raise Exception("Error generating payment link: " + response_data.get('message', 'Unknown error'))

    async def get_pay_status(self, order_id: str) -> bool:
        """
        Получает статус платежа по order_id.

        :param order_id: ID заказа.
        :return: Статус платежа (True - успешный, False - неуспешный).
        """
        async with aiohttp.ClientSession(headers=self.headers, timeout=self.timeout) as session:
            params = {'order_id': order_id, 'merchant_id': self.shop_id}
            response = await session.post(url="https://aaio.io/api/info-pay", data=params)
            response.raise_for_status()  # Проверка на наличие ошибок
            resp = await response.json()

            if resp.get('type') == "success":
                return resp['status'] in ["success", "hold"]
            return False  # Если тип не success, возвращаем False
