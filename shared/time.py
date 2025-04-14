from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc)

def date_from_string(value):
    return datetime.strptime(value, "%Y-%m-%d")

def datetime_from_string(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f%z")

def testing_datetime(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")

def now_testing():
    return datetime.now()