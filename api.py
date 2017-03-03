#!.env/bin/python
from flask import Flask, request
from flask_cors import CORS, cross_origin
from random import randint
import config
import requests 

matrix_switch_app_url = config.MATRIX_HOST + '/switch-app'
person_pick_url = config.MATRIX_HOST + '/person-picker'

app = Flask(__name__)
CORS(app)

@app.route('/mbta')
def mbta():
    requests.post(matrix_switch_app_url, data={'mode':'mbta'})
    return "Welcome to mbta"

@app.route('/person-picker')
def person_picker_switch():
    requests.post(matrix_switch_app_url, data={'mode':'person_picker'})
    return "Welcome to person-picker"

@app.route('/pick', methods=['POST'])
def person_picker():
    people = request.json['people']
    print people
    chosen_index = randint(0, len(people) - 1)
    print chosen_index
    requests.post(person_pick_url, data={'people': people, 'chosen_index':chosen_index})
    return "Person picked"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
