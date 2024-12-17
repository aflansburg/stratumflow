import time
from typing import Optional

import requests

from ..config.app_config import AppConfig
from ..config.logger import get_logger
from .helpers import generate_paubox_api_headers

app_config = AppConfig()

log = get_logger()

def get_subscribers(subscription_list_id: Optional[str] = None):
    RATE_LIMIT_SLEEP_TIME = 1
    ITEMS_PER_PAGE = 1000

    url = app_config.PAUBOX_MARKETING_API_URL + f"/subscribers"

    params = {"page": 1, "items": ITEMS_PER_PAGE}
    if subscription_list_id:
        params["subscription_list_id"] = subscription_list_id

    headers = generate_paubox_api_headers("marketing")
    subscribers = []

    init_request = requests.get(url, headers=headers, params=params)
    if init_request.status_code != 200:
        log.error(f"Failed to get subscribers: {init_request.status_code} {init_request.text}")
        raise Exception(f"Failed to get subscribers: {init_request.status_code} {init_request.text}")

    total_subscribers = init_request.json()["total_count"]

    while True:
        log.info(f"Requesting with params: {params}")

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            log.error(f"Failed to get subscribers: {response.status_code} {response.text}")
            raise Exception(f"Failed to get subscribers: {response.status_code} {response.text}")

        data = response.json()
        current_page_data = data.get("data", [])
        subscribers.extend(current_page_data)

        log.info(f"Total subscribers fetched so far: {len(subscribers)}")

        remaining_subscribers = total_subscribers - len(subscribers)
        if remaining_subscribers < ITEMS_PER_PAGE:
            params["items"] = remaining_subscribers

        if len(current_page_data) < ITEMS_PER_PAGE:
            break

        params["page"] += 1

        time.sleep(RATE_LIMIT_SLEEP_TIME)

    log.info(f"Total subscribers: {len(subscribers)}")

    unique_subscribers = []
    for subscriber in subscribers:
        if subscriber["id"] not in unique_subscribers:
            unique_subscribers.append(subscriber["id"])
        else:
            log.warning(f"Duplicate subscriber found: {subscriber['id']}")

    log.info(f"Total unique subscribers: {len(unique_subscribers)}")

    return unique_subscribers
