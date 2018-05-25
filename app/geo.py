
import requests
from pick import pick
from .settings import BING_KEY


def load_geocodes(city):
  print("loading geodata for {city}...".format(city=city))
  print("")
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
  for resource in resources:
    address = resource['address']
    city = address.get('formattedAddress', '')
    county = address.get('adminDistrict2', '')
    country = address.get('countryRegion', '')
    formatted_address = "{city}, {county} in {country}".format(city=city, county=county, country=country)
    options.append(formatted_address)
    items[formatted_address] = resource

  (option, index) = pick(options, title)
  
  return items[option]
