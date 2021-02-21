import os
from pyowm import OWM

def GetLocalWeather():
    owm = OWM(os.getenv("OPEN_WEATHER_APIKEY"))

    # Search for weather
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(os.getenv("WEATHER_PLACE"))
    weather = observation.weather

    return weather.weather_icon_name,weather.temperature('celsius')['temp']