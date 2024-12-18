import time
from typing import Optional

import requests

from ..config.app_config import AppConfig
from ..config.logger import get_logger
from .helpers import generate_paubox_api_headers

app_config = AppConfig()

log = get_logger()

# apparently you can only get 10000 subscribers maximum
# Paubox sends back a `search_after` parameter, that makes it seem
# like they're proxying Elasticsearch, so probably no way around
# this limit
def get_subscribers(subscription_list_id: Optional[str] = None):
    url = app_config.PAUBOX_MARKETING_API_URL + f"/subscribers"

    params = {}
    if subscription_list_id:
        params["subscription_list_id"] = subscription_list_id

    headers = generate_paubox_api_headers("marketing")

    init_request = requests.get(url, headers=headers, params=params)
    if init_request.status_code != 200:
        log.error(f"Failed to get subscribers: {init_request.status_code} {init_request.text}")
        raise Exception(f"Failed to get subscribers: {init_request.status_code} {init_request.text}")

    total_subscribers = init_request.json()["total_count"]
    log.info(f"Total subscribers: {total_subscribers}")

    subscribers = []
    
    params = {"page": 1, "items": total_subscribers}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        log.error(f"Failed to get subscribers: {response.status_code} {response.text}")
        raise Exception(f"Failed to get subscribers: {response.status_code} {response.text}")

    log.info(f"Response: {response.json()}")

    subscribers = response.json()["data"]

    return subscribers
