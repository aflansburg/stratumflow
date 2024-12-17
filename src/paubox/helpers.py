from ..config.app_config import AppConfig

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
