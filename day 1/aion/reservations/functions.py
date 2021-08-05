from datetime import datetime


def get_current_time(unix_time: float):
    return datetime.utcfromtimestamp(unix_time).strftime('%H:%M:%S')
