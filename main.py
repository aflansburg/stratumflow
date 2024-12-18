import base64
import json
import os
import importlib

import functions_framework
from cloudevents.http import CloudEvent


@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    try:
        message = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
        func_name = message.strip()

        module = importlib.import_module(f"src.functions.{func_name}")
        call_func = getattr(module, func_name)
        call_func()
    except Exception as e:
        if func_name and call_func is None:
            print(f"Function {func_name} not found")
            print(f"Error: {e}")
        else:
            print(f"Error: {e}")
        return


# for local testing
# if __name__ == "__main__":
#     from src.functions.refresh_all_user_subscription_list import (
#         refresh_all_user_subscription_list,
#     )

#     refresh_all_user_subscription_list()
