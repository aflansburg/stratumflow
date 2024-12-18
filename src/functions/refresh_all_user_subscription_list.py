from google.cloud import bigquery

from ..config.logger import get_logger
from ..paubox.subscribers import bulk_create_subscribers
from ..paubox.subscription_list import get_subscription_lists, delete_subscription_list

log = get_logger()


def refresh_all_user_subscription_list():
    client = bigquery.Client()

    query = """
    SELECT * FROM `data-platform-prod-431215.scratch.all_user_email`
    """

    query_job = client.query(query)
    results = query_job.result()

    log.info(f"Number of users: {results.total_rows}")

    list_name = "All Registered Users"

    list_id = next(
        (
            list["id"]
            for list in get_subscription_lists()["data"]
            if list["attributes"]["name"] == list_name
        ),
        None,
    )

    if list_id:
        log.info(f"Found List ID: {list_id}")

        delete_subscription_list(list_id)

    subscribers = results.to_dataframe().to_dict(orient="records")
    log.info(f"Subscribers count: {len(subscribers)}")

    result = bulk_create_subscribers(
        subscribers,
        should_create_subscription_list=True,
        subscription_list_name=list_name,
    )

    log.info(f"Result: {result}")
