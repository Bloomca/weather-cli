from .settings import check_keys
from .geo import load_geocodes
from .input import get_city, choose_resource
from .forecast import load_forecast
from .render import print_current_weather

def get_city_data():
  city = get_city()
  geocodes = load_geocodes(city)
  resources = geocodes['resourceSets'][0]['resources']
  city_object = choose_resource(resources)
  forecast = load_forecast(city_object)
  print_current_weather(forecast)