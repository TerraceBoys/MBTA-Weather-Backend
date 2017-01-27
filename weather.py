import urllib
import json
import time
import traceback
import config
import requests

weather_url = 'http://api.wunderground.com/api/' + config.WEATHER_API_KEY + '/conditions/q/MA/Roxbury_Crossing.json'
matrix_url = config.MATRIX_HOST + '/weather'

def main():
    try:
        while True:
            grab_weather()
            send_to_matrix()
            time.sleep(300)
    except SystemExit:
        print "Thread terminated"
    except IOError:
        print "Caught IOError while Loading Weather - Trying Again"
        print traceback.print_exc()
        time.sleep(600)
        main()
    except:
        print "Caught unhandled exception in Weather.main"
        print traceback.print_exc()


def grab_weather():
    response = urllib.urlopen(weather_url)
    global weather_data
    weather_data = json.loads(response.read().decode())
    # print "Boston Weather:"
    # print weather_data['current_observation']['weather']
    # print weather_data['current_observation']['feelslike_f'] + " F"

def send_to_matrix():
    temp, color = weather_panel()
    requests.post(matrix_url, data={'temp': temp, 'r': color[0], 'g': color[1], 'b': color[2], 'jpeg':"sun2"})

def weather_panel():
    global weather_data
    temperature = int(float(weather_data['current_observation']['feelslike_f']))
    return str(temperature), get_temp_color(temperature)


# Determine display color for temperature
def get_temp_color(temp):
    if temp >= 90:
        return 255, 0, 0
    elif temp >= 80:
        return 255, 50, 0
    elif temp >= 70:
        return 255, 100, 0
    elif temp >= 60:
        return 255, 150, 250
    else:
        return 0, 0, 255


if __name__ == "__main__":
    main()
