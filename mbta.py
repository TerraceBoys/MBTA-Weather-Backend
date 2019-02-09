#!.env/bin/python
import time
import traceback
import config
import requests
import mbtaTimeDisplay
from datetime import datetime
import pytz
from dateutil import parser

train_url = "https://api-v3.mbta.com/predictions?api_key=" + config.MBTA_API_KEY + "&sort=departure_time&filter[route_type]=0&filter[stop]=place-"
bus_url = "https://api-v3.mbta.com/predictions?api_key=" + config.MBTA_API_KEY + "&sort=departure_time&filter[direction_id]=1&filter[route_type]=3&filter[stop]=2586&filter[route]=87"
matrix_url = config.MATRIX_HOST + '/mbta'
allie_matrix_url = config.ALLIE_MATRIX_HOST + '/mbta'
train_times = []
bus_times = []
stationConverter = {'Forrest': 'forhl', 'Green': 'grnst', 'Stony': 'sbmnl', 'Jackson': 'jaksn', 'Roxbury': 'rcmnl',
                    'Ruggles': 'rugg', 'Mass': 'masta', 'Back': 'bbsta', 'Tufts': 'nemnl', 'Chinatown': 'chncl',
                    'Downtown': 'dwnxg', 'State': 'state', 'Haymarket': 'haecl', 'North': 'north', 'Community': 'ccmnl',
                    'Sullivan': 'sull', 'Wellington': 'welln', 'Malden': 'mlmnl', 'Oak': 'ogmnl', 'Lechmere': 'lech'}

def main():
    try:
        while True:
            pop_list(train_times, 'Lechmere')
            pop_bus_list(bus_times, 'ignored')
            send_to_matrix(train_times)
            try:
                send_to_allie_matrix(bus_times)
            except:
                print "Could not post to Allie"
            time.sleep(15)
    except IOError:
        print "Caught IOError"
        print traceback.print_exc()
        time.sleep(15)
        main()
    except KeyError:
        print "Caught IOError"
        print traceback.print_exc()
        time.sleep(15)
        main()
    except ValueError:
        print traceback.print_exc()
        time.sleep(60)
        main()
    except:
        print "Caught Unhandled exception in mbtajsonparse main"
        print traceback.print_exc()

def send_to_matrix(schedule):
    time_1, color_1, time_2, color_2 = mbtaTimeDisplay.panel_train(schedule)
    print time_1
    print time_2
    r = requests.post(matrix_url, data= {'time_1':time_1, 'color_1':color_1, 'time_2':time_2, 'color_2':color_2})

def send_to_allie_matrix(schedule):
    time_1, color_1, time_2, color_2 = mbtaTimeDisplay.panel_bus(schedule)
    print time_1
    print time_2
    r = requests.post(allie_matrix_url, data= {'time_1':time_1, 'color_1':color_1, 'time_2':time_2, 'color_2':color_2})

def get_station_json(station):
    r = requests.get(train_url + stationConverter[station])
    if 'data' in r.json():
       return r.json()['data']
    else:
       return []

def get_bus_json(station):
    r = requests.get(bus_url)
    if 'data' in r.json():
       return r.json()['data']
    else:
       return []

def pop_list(current_list, station):
    train_data = get_station_json(station)
    global train_times
    train_times = []
    for train in train_data:
        if train['attributes']['departure_time']:
            now = datetime.now(pytz.utc)
            arrival = parser.parse(train['attributes']['departure_time'])
            train_times.append((arrival - now).seconds)

def pop_bus_list(bus_list, station):
    bus_data = get_bus_json(station)
    global bus_times
    bus_times = []
    for bus in bus_data:
       if bus['attributes']['departure_time']:
            now = datetime.now(pytz.utc)
            arrival = parser.parse(bus['attributes']['departure_time'])
            bus_times.append((arrival - now).seconds)

if __name__ == "__main__":
    main()
