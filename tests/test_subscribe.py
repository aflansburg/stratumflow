from unittest.mock import patch
import base64
from cloudevents.http import CloudEvent
from main import subscribe

@patch('src.functions.refresh_all_user_subscription_list')
def test_subscribe(mock_google_cloud_function, capfd):
    mock_google_cloud_function.return_value = None

    attributes = {
        "type": "com.example.someevent",
        "source": "//event.source",
    }

    message_data = base64.b64encode(b"refresh_all_user_subscription_list").decode(
        "utf-8"
    )

    data = {"message": {"data": message_data}}

    event = CloudEvent(attributes, data)

    subscribe(event)

    captured = capfd.readouterr()

    assert "refresh_all_user_subscription_list" in captured.out
