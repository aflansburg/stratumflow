from google.cloud import bigquery

from ..config.logger import get_logger

log = get_logger()

def refresh_all_user_subscription_list():
    client = bigquery.Client()

    log.info("refresh_all_user_subscription_list")
