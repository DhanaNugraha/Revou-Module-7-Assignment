from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).isoformat()


def testing_datetime(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")

def now_testing():
    return datetime.now()