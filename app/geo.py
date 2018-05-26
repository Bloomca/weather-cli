
import requests
from .settings import BING_KEY

def load_geocodes(city):
  """
  Load geocodes for all cities with this name.
  There will be (probably) more than one city.
  """
  print("Loading geodata for {city}...".format(city=city))
  params = {
    'key': BING_KEY,
    'locality': city,
    'maxResults': 20
  }
  r = requests.get('http://dev.virtualearth.net/REST/v1/Locations', params=params)
  return r.json()
