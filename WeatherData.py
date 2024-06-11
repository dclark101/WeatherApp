import requests
import os
from dotenv import dotenv_values

CONFIG = dotenv_values(".env")


class WeatherData:
    def __init__(self):
        self.API_KEY = CONFIG["API_KEY"]
        print(self.API_KEY)

    def getWeatherData(self, by):
        res = requests.get(self.weatherURL(self.API_KEY, by))
        data = res.json()

        return data

    def weatherURL(self, appid, q) -> str:
        """Returns a URL of the OpenWeatherMap API that specifies the city and API_KEY

        Args:
            appid (string): API_KEY
            q (string): city
        """

        url = f"https://api.openweathermap.org/data/2.5/weather?appid={appid}&q={q}"

        return url
