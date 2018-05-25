import datetime

import requests
from pytz import timezone

from .geo import get_city_coords, format_city
from .settings import DARKSKY_KEY
from .debug import print_json

def load_forecast(city):
  print("loading forecast for {city}\n".format(city=format_city(city)))
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

def render_hourly_part(part, tz):
  f_temp = part['temperature']
  c_temp = f_to_c(f_temp)
  summary = part['summary']

  date = datetime.datetime.fromtimestamp(part['time'], tz=tz)
  localFormat = "%A, %d %B %Y, %H:%M:%S %z"

  return """{date}
  Right now it is {celcius}°C / {fahrenheit}°F.
  {summary}
  """.format(celcius=round(c_temp), fahrenheit=round(f_temp), summary=summary, date=date.strftime(localFormat))

def render_daily_part(part, tz):
  f_temp = part['temperature']
  c_temp = f_to_c(f_temp)
  summary = part['summary']

  date = datetime.datetime.fromtimestamp(part['time'], tz=tz)
  localFormat = "%A, %d %B %Y, %H:%M %z"

  return """{date}
  Right now it is {celcius}°C / {fahrenheit}°F.
  {summary}
  """.format(celcius=round(c_temp), fahrenheit=round(f_temp), summary=summary, date=date.strftime(localFormat))

def print_current_weather(forecast):
  current_forecast = forecast['currently']
  tz = timezone(forecast['timezone'])
  today = render_hourly_part(part = current_forecast, tz=tz)
  
  print(today)

  hourly_tables = []
  hourly_values = []
  i = 0
  for part in forecast['hourly']['data']:
    i += 1

    if i % 3 == 0:
      date = datetime.datetime.fromtimestamp(part['time'], tz=tz)
      localFormat = "%a %H:%M"
      f_temp = part['temperature']
      c_temp = f_to_c(f_temp)

      hourly_value = [
        date.strftime(localFormat),
        "{celcius}°C/{fahrenheit}°F".format(celcius=round(c_temp), fahrenheit=round(f_temp)),
        part['summary']
      ]

      hourly_values.append(hourly_value)
      if i > 15:
        i = 0
        hourly_tables.append(hourly_values)
        hourly_values = []


  if len(hourly_values):
    hourly_tables.append(hourly_values)

  tables_hourly_values = []
  for hourly_table in hourly_tables:
    table_hourly_values = zip(*hourly_table)
    tables_hourly_values.append(table_hourly_values)
  
  for table in tables_hourly_values:
    for row in table:
      str = ""
      for value in row:
        str += " {value: <20} |".format(value=value)

      print(str)
    
    print("=" * 23 * 6)


  for part in forecast['daily']['data']:
    pass
