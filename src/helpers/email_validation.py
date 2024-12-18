from validate_email_address import validate_email

import logging

log = logging.getLogger(__name__)


def is_valid_email(email):
    log.info(f"Validating email: {email}")
    try:
        return validate_email(email, check_mx=True)
    except Exception:
        return False
