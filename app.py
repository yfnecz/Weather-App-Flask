import sys
import requests
from flask import Flask, render_template, request
from flask_restful import reqparse
import json
from urllib.parse import quote


app = Flask(__name__)


parser = reqparse.RequestParser()
parser.add_argument(
    'city_name',
    type=str,
    help="The city name is required!",
    required=True
)

weather_api_key = ''
weather_codes = []

with open("../api.key", "r") as api_file:
    weather_api_key = api_file.readline()

with open("weather_code.json", "r") as code_file:
    weather_codes = json.loads(code_file.read())


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        city = request.form.get('city_name')
        api_url = f'https://api.tomorrow.io/v4/weather/realtime?location={quote(city)}&apikey={weather_api_key}'
        response = requests.get(api_url)
        if response.status_code == requests.codes.ok:
            weather = json.loads(response.text)
            temp = int(weather['data']['values']['temperature'])
            state = weather_codes[str(weather['data']['values']['weatherCode'])]
            weather = {'city': city, 'temp': temp, 'state': state}
            return render_template('index.html', weather=weather)
        else:
            return f"Error: {response.status_code}, {response.text}"



@app.route('/profile')
def profile():
    return 'This is profile page'


@app.route('/login')
def log_in():
    return 'This is login page'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

