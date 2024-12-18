import base64
import importlib
import os
import functions_framework
from cloudevents.http import CloudEvent


def call_function_from_message(message: str) -> None:
    try:
        namespace, func_name = message.strip().split(":")
        module = importlib.import_module(f"src.functions.{namespace}.{func_name}")
        call_func = getattr(module, func_name)
        call_func()
    except Exception as e:
        if func_name and call_func is None:
            print(f"Function {func_name} not found in namespace {namespace}")
        print(f"Error: {e}")


@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    try:
        message = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
        call_function_from_message(message)
    except Exception as e:
        print(f"Error: {e}")
        return


############ L O C A L   T E S T I N G #################################
if __name__ == "__main__" and os.getenv("ENV") == "dev":
    import sys
    from src.config.logger import get_logger

    log = get_logger()

    if len(sys.argv) != 2:
        log.error("Usage: python main.py <namespace:function_name>")
        sys.exit(1)

    message = sys.argv[1]
    log.debug(f"Received message: {message}")
    call_function_from_message(message)
########################################################################
