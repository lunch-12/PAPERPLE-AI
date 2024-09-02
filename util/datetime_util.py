from datetime import datetime, timezone, timedelta


def convert_NAVER_date_to_datetime(date_str: str) -> datetime:
    if "오전" in date_str:
        date_str = date_str.replace("오전", "AM")
    elif "오후" in date_str:
        date_str = date_str.replace("오후", "PM")

    date_format = "%Y.%m.%d. %p %I:%M"
    date_obj = datetime.strptime(date_str, date_format)

    return date_obj.replace(tzinfo=timezone.utc)


def convert_Yahoo_date_to_datetime(date_str: str) -> datetime:
    # print("CONVERT YAHOO DATA BEFORE:", date_str)
    base_str = date_str[:-6].strip()  # 'GMT+9' 제거
    # print("SECOND BASE STR:", base_str)
    parsed_date = datetime.strptime(base_str, "%a, %b %d, %Y, %I:%M %p")
    # print("PARED DATE:", parsed_date)

    offset_hours = 9
    offset = timezone(timedelta(hours=offset_hours))
    # print("OFFSET:", offset)
    parsed_date = parsed_date.replace(tzinfo=offset)
    # print("FINAL PARSED DATE:", parsed_date)

    return parsed_date