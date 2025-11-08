import re
from datetime import datetime


def extract_date(text: str) -> datetime | None:
    match = re.search(r"(\d{2}\.\d{2}\.\d{4})", text)
    if not match:
        return None

    date_str = match.group(1)

    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return None
