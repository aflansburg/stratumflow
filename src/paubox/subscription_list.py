import requests
from ..config.app_config import AppConfig
from ..config.logger import get_logger
from .helpers import generate_paubox_api_headers

app_config = AppConfig()

log = get_logger()


def get_subscription_lists():
    url = app_config.PAUBOX_MARKETING_API_URL + "/subscription_lists"
    log.info(f"Getting subscription list from {url}")
    headers = generate_paubox_api_headers("marketing")
    response = requests.get(url, headers=headers)

    log.info(f"Response: {response.status_code} {response.text}")
    if response.status_code != 200:
        raise Exception(
            f"Failed to get subscription list: {response.status_code} {response.text}"
        )

    return response.json()


def create_subscription_list(name: str):
    url = app_config.PAUBOX_MARKETING_API_URL + "/subscription_lists"

    log.info(f"Creating subscription list {name} at {url}")

    headers = generate_paubox_api_headers("marketing")
    response = requests.post(url, headers=headers, json={"name": name})

    if response.status_code != 200:
        raise Exception(
            f"Failed to create subscription list: {response.status_code} {response.text}"
        )
    return response.json()


def delete_subscription_list(subscription_list_id: str):
    url = (
        app_config.PAUBOX_MARKETING_API_URL
        + f"/subscription_lists/{subscription_list_id}"
    )
    log.info(f"Deleting subscription list {subscription_list_id} at {url}")
    headers = generate_paubox_api_headers("marketing")
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to delete subscription list: {response.status_code} {response.text}"
        )
    log.info(f"Subscription list deleted: {response.json()}")
    return response.json()
