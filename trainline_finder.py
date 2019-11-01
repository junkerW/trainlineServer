from typing import List
from datetime import datetime
import trainline
import pprint


def get_trainline(start_station, destination, start_time_there, end_time_there, bus=True, train=True):
    # results = []
    # for destination in destinations:
    transport = None
    if bus and train:
        transport = None
    elif bus:
        transport = 'coach'
    elif train:
        transport = 'train'

    result = trainline.search(
        departure_station=start_station,
        arrival_station=destination,
        from_date=start_time_there,
        to_date=end_time_there,
        transportation_mean=transport)
    # results.append({destination: csv2dict(result.csv())})
    # res_array = result.csv().split('\n')[1:].split(';')
    # results.append(res_array)

    # print("{}: \n{}".format(destination, result.csv()))
    return {'Start': start_station,
            'Destination': destination,
            'Connections': csv2dict(result.csv())}


def csv2dict(csv_str: str):
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


def sort_price(result: dict):
    connection = result['Connections']
    for conn in connection:
        if type(conn['price']) == type(''):
            conn['price'] = float(conn['price'].replace(',', '.'))
    result['Connections'] = sorted(connection, key=lambda k: k['price'] if k['price'] is not None else 1000)
    return result


def find_key_value(results: List[dict], key, value):
    for result in results:
        if result[key] == value:
            return result


def filter_duration(result, max_value):
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


def get_cheapest_round(theres: List[dict], backs: List[dict]):
    rounds = []
    for city_there in theres:
        try:
            city_back = find_key_value(backs, 'Start', city_there['Destination'])
            price_there = city_there['Connections'][0]['price']
            price_back = city_back['Connections'][0]['price']
            conn_there = city_there['Connections'][0]
            conn_back = city_back['Connections'][0]
            rounds.append({'City': city_there['Destination'],
                           'price': round(price_there + price_back, 2),
                           'Connection_there': conn_there,
                           'Connection_back': conn_back})
        except Exception as e:
            print("Error finding {} in backs: {}".format(city_there['Destination'], e))
            rounds.append({'City': city_there['Destination'],
                           'price': -1,
                           'Connection_there': '',
                           'Connection_back': ''})

    return sorted(rounds, key=lambda k: k['price'] if k['price'] is not None else 1000)

def __date2str(date:datetime):
    return date.strftime("%d/%m/%Y %H:%M")


def find_cheapest_connections(start_station, city_list, start_date_towards: datetime, end_date_towards: datetime,
                              start_date_back:datetime, end_date_back:datetime, max_duration: int = 24 * 60, bus=True, train=True):

    start_date_towards = __date2str(start_date_towards)
    end_date_towards = __date2str(end_date_towards)
    start_date_back = __date2str(start_date_back)
    end_date_back = __date2str(end_date_back)

    results_there = []
    results_back = []
    for destination in city_list:
        print("Finding connections for " + destination)
        try:
            results_there.append(get_trainline(start_station, destination, start_date_towards, end_date_towards, bus=bus, train=train))
        except Exception as e:
            print(e)

        try:
            results_back.append(get_trainline(destination, start_station, start_date_back, end_date_back, bus=bus,train=train))
        except Exception as e:
            print(e)

    results_there_filtered = []
    results_back_filtered = []

    print("Filter duration > " + str(max_duration))

    for result_there in results_there:
        results_there_filtered.append(filter_duration(result_there, max_duration))

    for result_back in results_back:
        results_back_filtered.append(filter_duration(result_back, max_duration))

    print("Sorting for lowest price")

    results_there_sorted = []
    results_back_sorted = []

    for result_there in results_there_filtered:
        results_there_sorted.append(sort_price(result_there))

    for result_back in results_back_filtered:
        results_back_sorted.append(sort_price(result_back))

    #pprint.pprint(results_there_sorted)
    #pprint.pprint(results_back_sorted)

    print("\nFinding cheapest Roundtrip")

    return get_cheapest_round(results_there_sorted, results_back_sorted)


