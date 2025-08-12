from datetime import datetime
import pandas as pd

from src.config import get_logger

log = get_logger()


def parse_date(date_str):
    if date_str in ["N/A", "<N/A", "", None]:
        return ""

    # Check if the input is a pandas.Timestamp
    if isinstance(date_str, pd.Timestamp):
        date_str = date_str.isoformat()

    if not isinstance(date_str, str):
        date_str = str(date_str)

    try:
        if "T" in date_str:
            # Return ISO 8601 format
            return datetime.fromisoformat(date_str).isoformat()
        else:
            # Try parsing w/ timezone information
            try:
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f%z").isoformat()
            except ValueError:
                # Try parsing w/o timezone information
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f").isoformat()
    except ValueError:
        log.debug(f"Invalid date provided to `parse_date`: {date_str}")
        return ""
