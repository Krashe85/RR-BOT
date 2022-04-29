import datetime


def get_dt_from_iso8601_string(dt_str):
    if "." in dt_str:
        dt, _, us = dt_str.partition(".")
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        us = int(us.rstrip("Z"), 10)
        return dt + datetime.timedelta(microseconds=us)
    elif "Z" in dt_str:
        dt = dt_str.rstrip("Z")
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        return dt
    elif "T" in dt_str:
        dt = dt_str.rstrip("Z")
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        return dt
    else:
        dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
        return dt


def generate_range_dates(start_date: datetime.datetime | datetime.date,
                         end_date: datetime.datetime | datetime.date) -> list[datetime.datetime | datetime.date]:
    date_1 = min(start_date, end_date)
    date_2 = max(start_date, end_date)

    items = [date_1]

    while date_1 < date_2:
        date_1 += datetime.timedelta(days=1)
        items.append(date_1)

    return items
