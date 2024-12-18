from datetime import datetime

from ..config.logger import get_logger

log = get_logger()


def parse_date(date_str):
    if date_str in ["N/A", "<N/A", "", None]:
        return ""
    try:
        if "T" in date_str:
            return datetime.fromisoformat(date_str).strftime("%Y-%m-%d %H:%M:%S")
        else:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f %Z").strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    except ValueError:
        log.warning(f"Invalid date provided to `parse_date`: {date_str}")
        return ""
