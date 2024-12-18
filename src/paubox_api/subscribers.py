from typing import Optional, List

import requests

from ..config.app_config import AppConfig
from ..config.logger import get_logger
from .helpers import generate_paubox_api_headers, validate_subscriber
from .subscription_list import create_subscription_list
from ..helpers.email_validation import is_valid_email

app_config = AppConfig()

log = get_logger()


# apparently you can only batch request subscribers - pagination does not work
# in the Paubox Marketing API (looks like a WIP)
# Paubox sends back a `search_after` parameter, that makes it seem
# like they're proxying Elasticsearch, so probably no way around
# this limit
def get_subscribers(subscription_list_id: Optional[str] = None) -> dict:
    url = app_config.PAUBOX_MARKETING_API_URL + "/subscribers"

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

    valid_subscribers, invalid_subscribers = [], []

    for index, subscriber in enumerate(subscribers):
        if index % 100 == 0:
            log.info(f"Validating subscriber at index: {index}")

        (
            valid_subscribers
            if is_valid_email(subscriber["email"], ignore_common=True)
            else invalid_subscribers
        ).append(subscriber)

    log.info(f"Valid subscribers count: {len(valid_subscribers)}")
    log.info(
        f"Invalid subscribers count: {len(invalid_subscribers)}\nInvalid Sample: {invalid_subscribers[:5]}"
    )

    return valid_subscribers, invalid_subscribers


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

    invalid_subscribers, validated_subscribers = [], []

    log.info(f"Validating {len(subscribers)} subscribers")
    for index, subscriber in enumerate(subscribers):
        if index % 100 == 0:
            log.info(f"Validating subscriber at index: {index}")
            log.info(
                f"Current validated subscribers count: {len(validated_subscribers)}"
            )
            log.info(f"Current invalid subscribers count: {len(invalid_subscribers)}")

        if is_valid_email(subscriber["email"], ignore_common=True):
            validated_subscribers.append(validate_subscriber(subscriber))
        else:
            invalid_subscribers.append(subscriber)

    log.warning(f"Removed {len(invalid_subscribers)} invalid subscribers")
    log.warning(f"Invalid Sample: {invalid_subscribers[:5]}")

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
