import requests

class DonationAlertsAPI:
    def __init__(self, api_token: str) -> None:
        self.api_token: str = api_token

    async def generate_pay_link(self, amount: float):
        url = "https://www.donationalerts.com/api/v1/alerts/donations"
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }
        requests.get(url=url, headers=headers)

def get_donation_alerts_api():
    # Импортируем settings только здесь, чтобы избежать циклического импорта
    from ..bot_settings import settings
    return DonationAlertsAPI(api_token=settings.DONATION_ALERTS_API_TOKEN)
