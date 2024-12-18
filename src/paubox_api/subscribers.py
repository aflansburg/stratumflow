from typing import Optional, List

import requests

from ..config.app_config import AppConfig
from ..config.logger import get_logger
from .helpers import generate_paubox_api_headers, validate_subscriber
from .subscription_list import create_subscription_list

app_config = AppConfig()

log = get_logger()


# apparently you can only get 10000 subscribers maximum
# Paubox sends back a `search_after` parameter, that makes it seem
# like they're proxying Elasticsearch, so probably no way around
# this limit
def get_subscribers(subscription_list_id: Optional[str] = None) -> dict:
    url = app_config.PAUBOX_MARKETING_API_URL + f"/subscribers"

    params = {}
    if subscription_list_id:
        params["subscription_list_id"] = subscription_list_id

    headers = generate_paubox_api_headers("marketing")

    init_request = requests.get(url, headers=headers, params=params)
    if init_request.status_code != 200:
        log.error(
            f"Failed to get subscribers: {init_request.status_code} {init_request.text}"
        )
        raise Exception(
            f"Failed to get subscribers: {init_request.status_code} {init_request.text}"
        )

    total_subscribers = init_request.json()["total_count"]
    log.info(f"Total subscribers: {total_subscribers}")

    subscribers = []

    params = {"page": 1, "items": total_subscribers}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        log.error(f"Failed to get subscribers: {response.status_code} {response.text}")
        raise Exception(
            f"Failed to get subscribers: {response.status_code} {response.text}"
        )

    log.info(f"Response: {response.json()}")

    subscribers = response.json()["data"]

    return subscribers


def bulk_create_subscribers(
    subscribers: List[dict],
    subscription_list_id: Optional[str] = None,
    should_create_subscription_list: Optional[bool] = False,
    subscription_list_name: Optional[str] = None,
) -> dict:
    if should_create_subscription_list:
        if not subscription_list_name:
            log.error("Subscription list name is required")
            raise Exception("Subscription list name is required")
        subscription_list_response = create_subscription_list(subscription_list_name)
        subscription_list_id = subscription_list_response["data"]["id"]

        log.info(f"Subscription list created: {subscription_list_response}")

    if not subscribers:
        log.info("No subscribers to create")
        return
    if not subscription_list_id:
        log.error("Subscription list ID is required")
        raise Exception("Subscription list ID is required")

    validated_subscribers = []
    for subscriber in subscribers:
        validated_subscribers.append(validate_subscriber(subscriber))

    log.info(f"Validated subscribers count: {len(validated_subscribers)}")
    url = app_config.PAUBOX_MARKETING_API_URL + "/subscribers_bulk_create"
    log.info(f"Creating subscribers at {url}")

    headers = generate_paubox_api_headers("marketing")

    response = requests.post(
        url,
        headers=headers,
        json={
            "subscribers": validated_subscribers,
            "subscription_list_id": subscription_list_id,
        },
    )

    if response.status_code != 200:
        log.error(
            f"Failed to create subscribers: {response.status_code} {response.text}"
        )
        raise Exception(
            f"Failed to create subscribers: {response.status_code} {response.text}"
        )

    return response.json()
