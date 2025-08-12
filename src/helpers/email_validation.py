from email_validator import validate_email, EmailNotValidError

import logging

log = logging.getLogger(__name__)


def is_valid_email(email, ignore_common=False):
    common_emails = [
        "gmail.com",
        "yahoo.com",
        "aol.com",
        "hotmail.com",
        "icloud.com",
        "comcast.net",
        "msn.com",
        "outlook.com",
        "verizon.net",
        "sbcglobal.net",
        "att.net",
        "live.com",
        "me.com",
        "ymail.com",
        "mac.com",
        "cox.net",
        "bellsouth.net",
    ]
    try:
        domain = email.split("@")[-1] if "@" in email else email
        if ignore_common and domain in common_emails:
            return True  # Valid email (common domain)

        validate_email(email)
        return True  # Valid email
    except EmailNotValidError:
        return False  # Invalid email
