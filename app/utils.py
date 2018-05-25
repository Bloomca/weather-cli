import argparse

def format_city(city):
  """
  Format city object in a human-readable string.
  """
  address = city['address']
  city = address.get('formattedAddress', '')
  county = address.get('adminDistrict2', '')
  country = address.get('countryRegion', '')
  return "{city}, {county} in {country}".format(city=city, county=county, country=country)

def get_city_coords(city):
  point = city['point']['coordinates']
  return (point[0], point[1])

def c_to_f(temp):
  """
  Convert celcius temperature to fahrenheit.
  """
  return temp * 1.8 + 32

def f_to_c(temp):
  """
  Convert fahrenheit temperature to celcius.
  """
  return temp / 1.8 - 32 / 1.8

def format_temp(temperature):
  return (round(temperature), round(f_to_c(temperature)))

def get_args():
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--city", help="City to get weather")
  return vars(ap.parse_args())