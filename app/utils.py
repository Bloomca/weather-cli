import argparse
import datetime

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
  """
  Return arguments.
  """
  ap = argparse.ArgumentParser()
  ap.add_argument("-c", "--city", help="City to get weather")
  return vars(ap.parse_args())

def create_date_tz(timestamp, tz):
  """
  Create datetime object from timestamp and timezone.
  """
  return datetime.datetime.fromtimestamp(timestamp, tz=tz)

def break_text(text, length, min = 1):
  """
  Break text into several lines, no longer than given length.
  """

  result = []
  while True:
    if len(text) < length:
      if text:
        result.append(text.lstrip())
      if len(result) < min:
        for x in range(0, min - len(result)):
          result.append("")
      return result

    part_text = text[:length]
    text = text[length:]

    if text == ".":
      text = ""
      part_text += "."
    
    result.append(part_text.lstrip())

def calculate_min(collection, get_text, length, columns):
  """
  Calculate number of rows to display table correctly.

  """
  result = []
  min = 1
  index = 0
  for item in collection:
    index += 1
    text = get_text(item)
    if (len(text) - 1) % length == 0:
      item_min = (len(text) - 1) // length
    else:
      item_min = (len(text) - 1) // length + 1

    if item_min > min:
      min = item_min

    if index == columns:
      index = 0
      result.append(min)
      min = 1

  if index != 0:
    result.append(min)
  
  return result

def print_underscore(text):
  print("\033[4m" + text + "\033[0;0m")

