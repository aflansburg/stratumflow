import base64
import importlib

import functions_framework
from cloudevents.http import CloudEvent


@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    try:
        message = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
        namespace, func_name = message.strip().split(":")

        module = importlib.import_module(f"src.functions.{namespace}.{func_name}")
        call_func = getattr(module, func_name)
        call_func()
    except Exception as e:
        if func_name and call_func is None:
            print(f"Function {func_name} not found in namespace {namespace}")
            print(f"Error: {e}")
        else:
            print(f"Error: {e}")
        return


############ L O C A L   T E S T I N G #################################
# if __name__ == "__main__":
#     from src.config.logger import get_logger

#     log = get_logger()

#     log.debug("Starting local test")
#     from src.functions.paubox.refresh_all_user_subscription_list import (
#         refresh_all_user_subscription_list,
#     )

#     refresh_all_user_subscription_list()
########################################################################
