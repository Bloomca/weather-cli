import datetime

import requests
from pytz import timezone

from .geo import get_city_coords, format_city
from .settings import DARKSKY_KEY

def load_forecast(city):
  """
  Loading forecast for the chosen city, using its
  latitude and longitude.
  More about API – https://darksky.net/dev/docs#/dev/docs#api-request-types
  """
  print("loading forecast for {city}\n".format(city=format_city(city)))
  (latitude, longitude) = get_city_coords(city)
  url = "https://api.darksky.net/forecast/{key}/{latitude},{longitude}".format(
    key=DARKSKY_KEY, latitude=latitude, longitude=longitude
  )

  r = requests.get(url)
  return r.json()

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

def render_hourly_part(part, tz):
  (f_temp, c_temp) = format_temp(part['temperature'])

  date = datetime.datetime.fromtimestamp(part['time'], tz=tz)
  summary = part['summary']
  localFormat = "%A, %d %B %Y, %H:%M:%S %z"

  return """{date}
  Right now it is {celcius}°C / {fahrenheit}°F.
  {summary}
  """.format(celcius=c_temp, fahrenheit=f_temp,
             summary=summary, date=date.strftime(localFormat))

def render_daily_part(part, tz):
  (f_temp, c_temp) = format_temp(part['temperature'])

  date = datetime.datetime.fromtimestamp(part['time'], tz=tz)
  summary = part['summary']
  localFormat = "%A, %d %B %Y, %H:%M %z"

  return """{date}
  Right now it is {celcius}°C / {fahrenheit}°F.
  {summary}
  """.format(celcius=c_temp, fahrenheit=f_temp,
             summary=summary, date=date.strftime(localFormat))

def print_today(forecast, tz):
  """
  Print hourly data for the next couple days.
  This function prints several tables with 6 columns max,
  so they don't overflow on the terminal screen.
  """

  # we need separate tables, so table does not overflow
  hourly_tables = []
  hourly_values = []
  i = 0
  for part in forecast['hourly']['data']:
    i += 1

    # we don't want to show weather for every hour, so we pick
    # only every 3rd hour
    if i % 3 == 0:
      date = datetime.datetime.fromtimestamp(part['time'], tz=tz)
      localFormat = "%a %H:%M"
      
      (f_temp, c_temp) = format_temp(part['temperature'])

      hourly_value = [
        date.strftime(localFormat),
        "{celcius}°C/{fahrenheit}°F".format(celcius=c_temp, fahrenheit=f_temp),
        part['summary']
      ]

      hourly_values.append(hourly_value)
      # 6 columns is enough, otherwise won't fit into a regular
      # terminal screen, so we break our data into several tables
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
        # to make it like a real table, we need to have
        # the same width, so we enforce string length
        str += " {value: <20} |".format(value=value)

      print(str)
    
    # draw a separator after each table
    # 20 for padded value, 2 space, 1 for "|" symbol
    # 6 for number of columns
    print("=" * 23 * 6)

def print_current_weather(forecast):
  current_forecast = forecast['currently']

  # we need to have timezones attached in order to
  # show local time – this is what is important to us
  tz = timezone(forecast['timezone'])
  right_now = render_hourly_part(part = current_forecast, tz=tz)
  
  print(right_now)
  print_today(forecast, tz)

  for part in forecast['daily']['data']:
    pass
