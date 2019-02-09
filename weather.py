#!.env/bin/python
import time
import traceback
import config
import requests
import backoff

weather_url = 'http://api.wunderground.com/api/' + config.WEATHER_API_KEY + '/conditions/q/MA/Cambridge.json'
matrix_url = config.MATRIX_HOST + '/weather'
allie_matrix_url = config.ALLIE_MATRIX_HOST + '/weather'

def main():
    try:
        while True:
            weather_data = grab_weather()
            send_to_matrix(weather_data)
            time.sleep(600)
    except IOError:
        print "Caught IOError while Loading Weather - Trying Again"
        print traceback.print_exc()
        time.sleep(600)
        main()
    except ValueError:
        print "Caught ValueError while Loading Weather - Trying Again"
        print traceback.print_exc()
        time.sleep(600)
        main()
    except:
        print "Caught unhandled exception in Weather.main"
        print traceback.print_exc()

@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=4)
def grab_weather():
    r = requests.get(weather_url)
    return r.json()
    # print "Boston Weather:"
    # print weather_data['current_observation']['weather']
    # print weather_data['current_observation']['feelslike_f'] + " F"

@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=4)
def send_to_matrix(weather_data):
    temp, color = weather_panel(weather_data)
    requests.post(matrix_url, data={'temp': temp, 'r': color[0], 'g': color[1], 'b': color[2], 'jpeg':"sun2"})
    try:
        requests.post(allie_matrix_url, data={'temp': temp, 'r': color[0], 'g': color[1], 'b': color[2], 'jpeg':"sun2"})
    except:
        print "Could not post to allie"

def weather_panel(weather_data):
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
