import logging
from settings import API_KEY

PROMO_FIVE_FILE = 'PROMO5.CSV'
EMAIL, TWITTER, CONTRACT = range(3)
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
HEADERS = {
    'X-CMC_PRO_API_KEY': API_KEY
    }
PARAMS = {
        'symbol': 'LCS'
    }

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
LOGGER = logging.getLogger(__name__)
DJANGO_URL = 'http://127.0.0.1:8000/en/register-chat-id/'