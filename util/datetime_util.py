from datetime import datetime, timezone


def convert_NAVER_date_to_datetime(date_str: str) -> datetime:
    if "오전" in date_str:
        date_str = date_str.replace("오전", "AM")
    elif "오후" in date_str:
        date_str = date_str.replace("오후", "PM")

    date_format = "%Y.%m.%d. %p %I:%M"
    date_obj = datetime.strptime(date_str, date_format)

    return date_obj.replace(tzinfo=timezone.utc)
