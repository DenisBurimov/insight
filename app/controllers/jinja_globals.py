from datetime import datetime


def time_without_seconds(datetime: datetime) -> str:
    return datetime.strftime("%Y-%m-%d %H:%M")
