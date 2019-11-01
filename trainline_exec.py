import trainline_finder as train
import pprint

start_date_towards = "01/11/2019 09:00"
end_date_towards = "01/11/2019 12:00"

start_date_back = "03/11/2019 12:00"
end_date_back = "03/11/2019 18:00"

start_station = 'Stuttgart'

max_duration = 6 * 60  # in min

destinations_str = []
city_file = open('city_list_2.txt')
for line in city_file.readlines():
    destinations_str.append(line.split(','))
city_file.close()

destinations = [f[1] for f in destinations_str]

city_file = open('city_list_4.txt')
destinations_str = city_file.read().split(',')
city_file.close()

for dest in destinations_str:
    destinations.append(dest)

final = train.find_cheapest_connections(start_station,destinations,start_date_towards,end_date_towards,
                                            start_date_back,end_date_back,max_duration)

pprint.pprint(final)
