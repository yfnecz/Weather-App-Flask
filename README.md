# [Weather-App-Flask](https://weather-app-flask-2f3w.onrender.com/)

Educational one-page Weather web app created using Python & Flask framework.

SQLite database is used for data storage.

Uses [OpenWeatherMap API](https://openweathermap.org/) to get real-time weather information.

Deployed using Render here:
[Check it out](https://weather-app-flask-2f3w.onrender.com/)

To run locally with Docker:
1) clone the repo
2) add api.key file to the root folder containing your API key to Open Weather Map API
3) use docker to build image:

`docker build -t weather-app .`

5) use docker to run locally:

`docker run -p 8080:8080 weather-app`

6) open http://127.0.0.1:8080

Here is how the app looks and works:

![ezgif-1-a27cc7d58c](https://github.com/user-attachments/assets/15819ef4-637d-45a4-b4d6-3c272cbf2c44)

