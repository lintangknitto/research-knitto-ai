from datetime import datetime
import pytz

def get_time_of_day():
    indonesian_tz = pytz.timezone("Asia/Jakarta")
    now = datetime.now(indonesian_tz)

    if 5 <= now.hour < 10:
        return "pagi"
    elif 10 <= now.hour < 15:
        return "siang"
    elif 15 <= now.hour < 18:
        return "sore"
    else:
        return "malam"
