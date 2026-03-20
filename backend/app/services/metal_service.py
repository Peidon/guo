import requests
from core.config import settings
from loguru import logger


def fetch_metal_price(symbol, curr, date = ""):
    """
    :param symbol: Metal Symbol "XAU", "XAG", "XPT", "XPD"
    :param curr: Currency Code "AUD", "USD" etc.
    :param date: "/20260318"
    :return:
    """

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

    headers = {
        "x-access-token": settings.METAL_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error("gold api error {x}", x=e)