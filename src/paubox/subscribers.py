import time
from typing import Optional

import requests

from ..config.app_config import AppConfig
from ..config.logger import get_logger
from .helpers import generate_paubox_api_headers

app_config = AppConfig()

log = get_logger()

def get_subscribers(subscription_list_id: Optional[str] = None):
    PAGE_SIZE = 50
    RATE_LIMIT_SLEEP_TIME = 1

    url = app_config.PAUBOX_MARKETING_API_URL + f"/subscribers"

    params = {}
    if subscription_list_id:
        params["subscription_list_id"] = subscription_list_id

    params["page"] = 1
    # params["items"] = 1

    log.info(f"Initial request to {url} with params {params} to ascertain total count")
    
    headers = generate_paubox_api_headers("marketing")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        log.error(f"Failed to get subscribers: {response.status_code} {response.text}")
        raise Exception(f"Failed to get subscribers: {response.status_code} {response.text}")

    total_count = response.json()["total_count"]

    log.info(f"Total subscribers to fetch: {total_count}")
    log.info(f"Total pages to fetch: {total_count // PAGE_SIZE}")

    subscribers = []
    for page in range(1, total_count // PAGE_SIZE + 1):
        log.info(f"Requesting page {page} of {total_count // PAGE_SIZE}")
        
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            log.error(f"Failed to get subscribers: {response.status_code} {response.text}")
            raise Exception(f"Failed to get subscribers: {response.status_code} {response.text}")

        data = response.json()["data"]
        
        subscribers.extend(data)
        
        time.sleep(RATE_LIMIT_SLEEP_TIME)
    
    log.info(f"Total subscribers: {len(subscribers)}")
    return subscribers
