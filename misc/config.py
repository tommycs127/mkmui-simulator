VALID_TIMEDELTA_KEYS = {
    'days',
    'seconds',
    'microseconds',
    'milliseconds',
    'minutes',
    'hours',
    'weeks',
}


def validate_time_format_json(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    for key, value in data.items():
        if key not in VALID_TIMEDELTA_KEYS:
            return False
        if not isinstance(value, (int, float)):
            return False
    return True
