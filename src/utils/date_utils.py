from datetime import datetime


def parse_date_time(value: str) -> datetime:
    return datetime.strptime(value, "%b %d, %Y %I:%M:%S %p")
