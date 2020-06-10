import logging
from settings import EXCHANGE_URL

PARAMS = {
        'symbol': 'LCS'
    }

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
