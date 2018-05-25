
import requests
from pick import pick
from .settings import BING_KEY

def format_city(city):
  """
  Format city object in a human-readable string.
  """
  address = city['address']
  city = address.get('formattedAddress', '')
  county = address.get('adminDistrict2', '')
  country = address.get('countryRegion', '')
  return "{city}, {county} in {country}".format(city=city, county=county, country=country)

def load_geocodes(city):
  """
  Load geocodes for all cities with this name.
  There will be (probably) more than one city.
  """
  print("loading geodata for {city}...".format(city=city))
  params = {
    'key': BING_KEY,
    'locality': city,
    'maxResults': 20
  }
  r = requests.get('http://dev.virtualearth.net/REST/v1/Locations', params=params)
  return r.json()

def get_city_coords(city):
  point = city['point']['coordinates']
  return (point[0], point[1])

def choose_resource(resources):
  title = 'Please choose desired city: '

  if len(resources) == 0:
    print("Sorry, no cities were found with this name")
    exit(1)

  if len(resources) == 1:
    return resources[0]

  options = []
  items = {}
  for city in resources:
    formatted_address = format_city(city)
    options.append(formatted_address)
    items[formatted_address] = city

  (option, index) = pick(options, title)
  
  return items[option]
