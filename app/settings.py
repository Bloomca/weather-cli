import os

BING_KEY = os.environ.get('BING_KEY')
DARKSKY_KEY = os.environ.get('DARKSKY_KEY')

def check_keys():
  if BING_KEY is None:
    print("You have to provide your Bing Maps Key")
    print("More info at https://www.bingmapsportal.com/")
    exit(1)

  if DARKSKY_KEY is None:
    print("You have to provide your DarkSky Maps Key")
    print("More info at https://darksky.net/dev")
    exit(1)