import requests
from .geo import get_city_coords
from .settings import DARKSKY_KEY

def load_forecast(city):
  (latitude, longitude) = get_city_coords(city)
  url = "https://api.darksky.net/forecast/{key}/{latitude},{longitude}".format(
    key=DARKSKY_KEY, latitude=latitude, longitude=longitude
  )

  r = requests.get(url)
  return r.json()

def c_to_f(temp):
  return temp * 1.8 + 32

def f_to_c(temp):
  return temp / 1.8 - 32 / 1.8

def print_current_weather(forecast):
  f_temp = forecast['currently']['temperature']
  c_temp = f_to_c(f_temp)

  print("Right now it is {celcius:.2f} Celcius degrees, and {fahrenheit} Fahrenheit degrees".format(
    celcius=c_temp, fahrenheit=f_temp
  ))