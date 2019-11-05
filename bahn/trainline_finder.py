from typing import List
from datetime import datetime
import trainline
import logging
from multiprocessing import Pool

from bahn.roundtrip import Trip


class TrainlineFinder:
    logger = None

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def get_trainline(self, trip: Trip, bus=True, train=True):
        # for destination in destinations:
        self.logger.info("Finding connections for " + trip.destination)
        transport = None
        if bus and train:
            transport = None
        elif bus:
            transport = 'coach'
        elif train:
            transport = 'train'

        result = trainline.search(
            departure_station=trip.start_station,
            arrival_station=trip.destination,
            from_date=trip.start_date_str,
            to_date=trip.end_date_str,
            transportation_mean=transport)
        # results.append({destination: csv2dict(result.csv())})
        # res_array = result.csv().split('\n')[1:].split(';')
        # results.append(res_array)

        # print("{}: \n{}".format(destination, result.csv()))
        return {'Start': trip.start_station,
                'Destination': trip.destination,
                'Connections': self._csv2dict(result.csv())}

    def _csv2dict(self, csv_str: str):
        rows = csv_str.split('\n')
        keys = rows[0].split(';')
        del rows[0]
        dictis = []
        for row in rows:
            dicti = {}
            if row != "":
                row = row.split(';')
                for key in range(len(keys)):
                    dicti[keys[key]] = row[key]
                dictis.append(dicti)
        return dictis

    def _sort_price(self, result: dict):
        connection = result['Connections']
        for conn in connection:
            if type(conn['price']) == type(''):
                conn['price'] = float(conn['price'].replace(',', '.'))
        result['Connections'] = sorted(connection, key=lambda k: k['price'] if k['price'] is not None else 1000)
        return result

    def _find_key_value(self, results: List[dict], key, value):
        for result in results:
            if result[key] == value:
                return result

    def _filter_duration(self, result, max_value):
        conn_out = []
        connection = result['Connections']
        for conn in connection:
            hour = int(conn['duration'].split('h')[0])
            minute = int(conn['duration'].split('h')[1])
            duration = hour * 60 + minute
            if duration < max_value:
                conn_out.append(conn)
            result['Connections'] = conn_out
        return result

    def _filter_cheapest_round(self, theres: List[dict], backs: List[dict]):
        rounds = []
        for city_there in theres:
            try:
                city_back = self._find_key_value(backs, 'Start', city_there['Destination'])
                price_there = city_there['Connections'][0]['price']
                price_back = city_back['Connections'][0]['price']
                conn_there = city_there['Connections'][0]
                conn_back = city_back['Connections'][0]
                rounds.append({'City': city_there['Destination'],
                               'price': round(price_there + price_back, 2),
                               'Connection_there': conn_there,
                               'Connection_back': conn_back})
            except Exception as e:
                self.logger.error("Error finding {} in backs: {}".format(city_there['Destination'], e))
                rounds.append({'City': city_there['Destination'],
                               'price': -1,
                               'Connection_there': '',
                               'Connection_back': ''})

        return sorted(rounds, key=lambda k: k['price'] if k['price'] is not None else 1000)

    def _run_destination_tasks(self, start_station, city_list, start_date_towards: datetime,
                               end_date_towards: datetime,
                               start_date_back: datetime, end_date_back: datetime, bus=True, train=True):
        round_trips = []
        for destination in city_list:  # Loop over all destinations
            round_trips.append([Trip(start_station, destination,
                                     start_date_towards, end_date_towards), bus,
                                train])
            round_trips.append([Trip(destination, start_station,
                                     start_date_back, end_date_back), bus,
                                train])

        with Pool(processes=20) as pool:
            results = pool.starmap(self.get_trainline, [trip for trip in round_trips])
        # round_tasks.append(self._create_round_tasks(round_trip, bus=bus, train=train))

        # for trip_task in round_task:
        # result = await asyncio.gather(*asyncio.gather(*round_task))
        # results = []
        # for trip_tasks in round_tasks:
        #     for trip in trip_tasks:
        #         results.append(trip.)
        return results

    def find_cheapest_roundtrips(self, start_station, city_list, start_date_towards: datetime,
                                 end_date_towards: datetime,
                                 start_date_back: datetime, end_date_back: datetime, max_duration: int = 24 * 60,
                                 bus=True, train=True):


        round_trips = self._run_destination_tasks(start_station, city_list,
                                                  start_date_towards, end_date_towards, start_date_back, end_date_back,
                                                  bus=bus, train=train)

        results_there = [trip for trip in round_trips if trip['Start'] == start_station]
        results_back = [trip for trip in round_trips if trip['Destination'] == start_station]
        results_there_filtered = []
        results_back_filtered = []

        self.logger.debug("Filter duration > " + str(max_duration))

        for result_there in results_there:
            results_there_filtered.append(self._filter_duration(result_there, max_duration))

        for result_back in results_back:
            results_back_filtered.append(self._filter_duration(result_back, max_duration))

        self.logger.debug("Sorting for lowest price")

        results_there_sorted = []
        results_back_sorted = []

        for result_there in results_there_filtered:
            results_there_sorted.append(self._sort_price(result_there))

        for result_back in results_back_filtered:
            results_back_sorted.append(self._sort_price(result_back))

        # pprint.pprint(results_there_sorted)
        # pprint.pprint(results_back_sorted)

        self.logger.debug("\nFinding cheapest Roundtrip")

        return self._filter_cheapest_round(results_there_sorted, results_back_sorted)
