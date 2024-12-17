import base64
from cloudevents.http import CloudEvent
from main import subscribe  # Import the function to be tested


def test_subscribe(capfd):
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
