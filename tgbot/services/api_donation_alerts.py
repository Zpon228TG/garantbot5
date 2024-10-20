import requests

from ..bot_settings import settings


class DonationAlertsAPI:
    def __init__(self, api_token: str) -> None:
        self.api_token: str = api_token

    async def generate_pay_link(self, amount: float):
        """
        Создает платежную ссылку для пополнения баланса.

        :param amount: Сумма пополнения баланса в профиле.
        :return: Платежная ссылка.
        """

        url = "https://www.donationalerts.com/api/v1/alerts/donations"

        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

        requests.get(url=url, headers=headers)


API_Donation_alerts = DonationAlertsAPI(api_token=settings.DONATION_ALERTS_API_TOKEN)
