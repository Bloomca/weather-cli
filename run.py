import argparse
from app.settings import BING_KEY, DARKSKY_KEY
from app.geo import load_geocodes, choose_resource
from app.forecast import load_forecast, print_current_weather

if BING_KEY is None:
  print("You have to provide your Bing Maps Key")
  print("More info at https://www.bingmapsportal.com/")
  exit(1)

if DARKSKY_KEY is None:
  print("You have to provide your DarkSky Maps Key")
  print("More info at https://darksky.net/dev")
  exit(1)

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--city", help="City to get weather")
args = vars(ap.parse_args())

def get_city():
  if 'city' in args and args['city'] is not None:
    return args['city']

  while True:
    answer = input('Please provide a city\n > ')
    print("")

    if len(answer) > 2:
      return answer
    else:
      print("Sorry, name should be more than 2 letters\n")

def get_city_data():
  city = get_city()
  geocodes = load_geocodes(city)
  resources = geocodes['resourceSets'][0]['resources']
  city_object = choose_resource(resources)
  forecast = load_forecast(city_object)

  print_current_weather(forecast)

if __name__ == "__main__":
  get_city_data()
