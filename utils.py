from datetime import datetime, timezone

def convert_time(time) -> datetime.time:
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z"
    ]
    for f in formats:
        try:
            return datetime.strptime(time, f).replace(tzinfo=timezone.utc)
        except Exception as e:
            continue
    raise ValueError(f"Неизвестный формат даты: {time}")

now = datetime.now(timezone.utc)
pub = convert_time('Wed, 21 Aug 2024 18:00:13 GMT')

print(pub>now)