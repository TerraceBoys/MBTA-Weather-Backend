#!.env/bin/python
from flask import Flask
from flask_cors import CORS, cross_origin
import config
import requests 

matrix_switch_app_url = config.MATRIX_HOST + '/switch-app'

app = Flask(__name__)
CORS(app)

@app.route('/mbta')
def index():
    requests.post(matrix_switch_app_url, data={'mode':'mbta'})
    return "Welcome to mbta"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
