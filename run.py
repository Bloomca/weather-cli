import argparse
from app.settings import BING_KEY, DARKSKY_KEY, check_keys
from app.geo import load_geocodes
from app.input import get_city, choose_resource
from app.forecast import load_forecast, print_current_weather

# we can't proceed without API keys
check_keys()

def get_city_data():
  city = get_city()
  geocodes = load_geocodes(city)
  resources = geocodes['resourceSets'][0]['resources']
  city_object = choose_resource(resources)
  forecast = load_forecast(city_object)
  print_current_weather(forecast)

if __name__ == "__main__":
  get_city_data()
