import datetime


class RoundTrip:

    trip_there = None
    trip_back = None

    def __init__(self, start_station, destination, start_date_towards: datetime, end_date_towards: datetime,
                 start_date_back: datetime, end_date_back: datetime):

        self.trip_there = Trip(start_station, destination, start_date_towards, end_date_towards)

        self.trip_back = Trip(destination, start_station, start_date_back, end_date_back)


def _date2str(date: datetime):
    return date.strftime("%d/%m/%Y %H:%M")


class Trip:

    start_station = None
    destination = None
    start_date = None
    end_date = None

    def __init__(self, start_station, destination, start_date: datetime, end_date: datetime):
        self.start_station = start_station
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_str = _date2str(start_date)
        self.end_date_str = _date2str(end_date)

