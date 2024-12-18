from ..config.app_config import AppConfig
from ..helpers.date_time_utils import parse_date

app_config = AppConfig()


def _get_paubox_api_key(api_type: str):
    if api_type == "email":
        return app_config.PAUBOX_EMAIL_API_KEY
    elif api_type == "marketing":
        return app_config.PAUBOX_MARKETING_API_KEY
    else:
        raise ValueError(f"Invalid API type: {api_type}")


def generate_paubox_api_headers(api_type: str):
    api_key = _get_paubox_api_key(api_type)
    return {
        "Authorization": f"Token token={api_key}",
        "Content-Type": "application/json",
    }


def validate_subscriber(subscriber: dict):
    if "email" not in subscriber or not isinstance(subscriber["email"], str):
        raise ValueError("The 'email' field is required and must be a string.")

    if "first_name" in subscriber and not isinstance(subscriber["first_name"], str):
        raise ValueError("The 'first_name' field must be a string.")

    if "last_name" in subscriber and not isinstance(subscriber["last_name"], str):
        raise ValueError("The 'last_name' field must be a string.")

    if "custom_fields" in subscriber:
        if not isinstance(subscriber["custom_fields"], list):
            raise ValueError("The 'custom_fields' field must be a list.")

        for field in subscriber["custom_fields"]:
            if not isinstance(field, dict):
                raise ValueError("Each item in 'custom_fields' must be a dictionary.")
            for key, value in field.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise ValueError(
                        "Each key and value in 'custom_fields' must be a string."
                    )

    created_at = parse_date(subscriber["created_at"])
    updated_at = parse_date(subscriber["updated_at"])

    return {
        "email": subscriber["email"],
        "first_name": subscriber["firstname"],
        "account_created": created_at,
        "last_visited": updated_at,
    }
