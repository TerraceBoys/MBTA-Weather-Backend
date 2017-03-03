#!.env/bin/python
import time
import traceback
import config
import requests
import backoff
import mbtaTimeDisplay
from collections import defaultdict

train_url = 'http://realtime.mbta.com/developer/api/v2/predictionsbystop?api_key=' + config.MBTA_API_KEY + '&stop=place-'
matrix_url = config.MATRIX_HOST + '/mbta'
schedule = defaultdict(list)
stationConverter = {'Forrest': 'forhl', 'Green': 'grnst', 'Stony': 'sbmnl', 'Jackson': 'jaksn', 'Roxbury': 'rcmnl',
                    'Ruggles': 'rugg', 'Mass': 'masta', 'Back': 'bbsta', 'Tufts': 'nemnl', 'Chinatown': 'chncl',
                    'Downtown': 'dwnxg', 'State': 'state', 'Haymarket': 'haecl', 'North': 'north', 'Community': 'ccmnl',
                    'Sullivan': 'sull', 'Wellington': 'welln', 'Malden': 'mlmnl', 'Oak': 'ogmnl'}


def main():
    try:
        while True:
            pop_dict(schedule, 'Roxbury')  # populate schedule dict
            send_to_matrix(schedule)
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

@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=4)
def send_to_matrix(schedule):
    time_1, color_1, time_2, color_2 = mbtaTimeDisplay.panel_train(schedule)
    print time_1
    print time_2
    r = requests.post(matrix_url, data= {'time_1':time_1, 'color_1':color_1, 'time_2':time_2, 'color_2':color_2})

@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=4)
def get_station_json(station):
    r = requests.get(train_url + stationConverter[station] + '&format=json')
    return r.json()


# Parse all Roxbury Crossing train arrival times
# Add all times to defaultdict (schedule)
def pop_dict(current_dict, station):
    train_data = get_station_json(station)
    current_dict.clear()

    if 'mode' in train_data:
        for x in range(len(train_data['mode'])):
            # If the mode is subway
            if train_data['mode'][x]['mode_name'] == 'Subway':
                # for each route
                for r in range(len(train_data['mode'][x]['route'])):
                    # if route name is orange line
                    if train_data['mode'][x]['route'][r]['route_name'] == 'Orange Line':
                        # for every direction
                        for y in range(len(train_data['mode'][x]['route'][r]['direction'])):
                            # For each train
                            for z in range(len(train_data['mode'][x]['route'][r]['direction'][y]['trip'])):
                                # add each train to the schedule dict -> schedule['direction'].append(pre_away)
                                current_dict[
                                    train_data['mode'][x]['route'][r]['direction'][y]['direction_name']].append(
                                    int(train_data['mode'][x]['route'][r]['direction'][y]['trip'][z]['pre_away']))
                break

if __name__ == "__main__":
    main()
