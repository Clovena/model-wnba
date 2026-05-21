import requests
import time
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba"
CORE_URL = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/wnba"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; wnba-mart-research/1.0)",
    "Accept": "application/json",
}

def get(endpoint: str, params: Optional[dict] = None, retries: int = 3) -> dict:
    """
    Make a GET request to an ESPN endpoint with retry logic.
    Returns parsed JSON or raises on unrecoverable failure.
    """
    url = f"{BASE_URL}/{endpoint}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(1)  # conservative rate limiting
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error on attempt {attempt + 1}: {e}")
            if response.status_code == 429:
                time.sleep(30)  # back off hard on rate limit
            elif attempt == retries - 1:
                raise
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed on attempt {attempt + 1}: {e}")
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)  # exponential backoff
    
def get_core(endpoint: str, params: Optional[dict] = None) -> dict:
    """
    Hit the core API for deeper data (play-by-play, etc.)
    """
    url = f"{CORE_URL}/{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    time.sleep(1)
    return response.json()