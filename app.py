import sys, requests, json, datetime
from flask import Flask, render_template, request, redirect, flash
from flask_restful import reqparse
from geopy.geocoders import Nominatim
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


db.create_all()

parser = reqparse.RequestParser()
parser.add_argument(
    'city_name',
    type=str,
    help="The city name is required!",
    required=True
)

weather_api_key = ''
weather_codes = []

with open("/Users/Natali/Documents/work/PycharmProjects/Weather App/Weather App/api.key", "r") as api_file:
    weather_api_key = api_file.readline()

geolocator = Nominatim(user_agent="abcd")


@app.route('/', methods=['GET', 'POST'])
def index():
    cities = []
    if request.method == 'POST':
        new_name = request.form.get('city_name')
        if City.query.filter_by(name=new_name).first() is None:
            location = geolocator.geocode(new_name)
            if location is not None:
                new_city = City(name=new_name)
                db.session.add(new_city)
                db.session.commit()
            else:
                flash("The city doesn't exist!")
        else:
            flash("The city has already been added to the list!")
    api_url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'
    for city in City.query.all():
        location = geolocator.geocode(city.name)
        response = requests.get(api_url.format(location.latitude, location.longitude, weather_api_key))
        if response.status_code == requests.codes.ok:
            weather = json.loads(response.text)
            temp = int(weather['main']['temp'])
            state = weather['weather'][0]['main']

            utc_now = datetime.datetime.fromtimestamp(weather['dt']) # time in utc seconds
            timezone = datetime.timezone(datetime.timedelta(seconds=weather['timezone']))
            hour = utc_now.astimezone(timezone).hour

            time_of_day = 'day' if 19 > hour > 11 else 'evening-morning'
            time_of_day = 'night' if hour < 5 or hour > 22 else time_of_day
            cities.append({'city': city.name, 'temp': temp, 'state': state, 'time_of_day': time_of_day, 'city_id': city.id})
        else:
            flash(f"Error: {response.status_code}, {response.text}")
    return render_template('index.html', cities=cities)


@app.route('/delete/<int:city_id>', methods=['POST'])
def delete_city(city_id):
    city = City.query.filter_by(id=city_id).first()
    if city:
        db.session.delete(city)
        db.session.commit()
    return redirect("/")



if __name__ == '__main__':
    app.secret_key = 'HelloWorld'
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

