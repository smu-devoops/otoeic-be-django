import datetime


HOUR_OF_START_OF_THE_DAY = 6


def get_date_range(of_datetime: datetime.datetime, divide_hour=HOUR_OF_START_OF_THE_DAY):
    today = of_datetime.date()
    if of_datetime.hour < divide_hour:
        today -= datetime.timedelta(days=1)
    date_min = datetime.datetime.combine(today, datetime.time(hour=divide_hour))
    date_max = date_min + datetime.timedelta(days=1)
    return (date_min, date_max)
