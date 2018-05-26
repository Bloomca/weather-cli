import datetime

import requests
from pytz import timezone

from .utils import (get_city_coords, format_city, print_underscore,
                    format_temp, create_date_tz, break_text, calculate_min)
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

def render_hourly_part(part, tz):
  (f_temp, c_temp) = format_temp(part['temperature'])

  date = create_date_tz(part['time'], tz)
  summary = part['summary']
  localFormat = "%A, %d %B %Y, %H:%M:%S %z"

  return """{date}
  Right now it is {celcius}°C / {fahrenheit}°F.
  {summary}
  """.format(celcius=c_temp, fahrenheit=f_temp,
             summary=summary, date=date.strftime(localFormat))

def render_daily_part(part, tz):
  (f_temp, c_temp) = format_temp(part['temperature'])

  date = create_date_tz(part['time'], tz)
  summary = part['summary']
  localFormat = "%A, %d %B %Y, %H:%M %z"

  return """{date}
  Right now it is {celcius}°C / {fahrenheit}°F.
  {summary}
  """.format(celcius=c_temp, fahrenheit=f_temp,
             summary=summary, date=date.strftime(localFormat))

def create_tables(data, make_values, skip, columns):
  """
  Create tables to display data in a console.
  """

  if skip < 1:
    raise ValueError("skip value should be at least 1")

  if columns < 1:
    raise ValueError("column value should be at least 1")

  # we need separate tables, so table does not overflow
  tables = []
  values = []
  i = 0
  for part in data:
    i += 1

    # we don't want to show weather for every hour, so we pick
    # only every 3rd hour
    if i % skip == 0:
      value = make_values(part, len(tables))
      values.append(value)
      # 6 columns is enough, otherwise won't fit into a regular
      # terminal screen, so we break our data into several tables
      if i > skip * (columns - 1):
        i = 0
        tables.append(values)
        values = []


  if len(values):
    tables.append(values)

  tables_values = []
  for table in tables:
    table_values = zip(*table)
    tables_values.append(table_values)

  return tables_values

def print_today(forecast, tz):
  """
  Print hourly data for the next couple days.
  This function prints several tables with 6 columns max,
  so they don't overflow on the terminal screen.
  """

  print_underscore(forecast['hourly']['summary'])
  print("")

  def create_values(part, index):
    date = create_date_tz(part['time'], tz)
    localFormat = "%a %H:%M"
    
    (f_temp, c_temp) = format_temp(part['temperature'])

    return [
      date.strftime(localFormat),
      "{celcius}°C/{fahrenheit}°F".format(celcius=c_temp, fahrenheit=f_temp),
      part['summary']
    ]

  data = forecast['hourly']['data']
  columns = 6
  tables_hourly_values = create_tables(data, create_values,
                                       skip = 3, columns = columns)
  
  padded_length = 20
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
    print("=" * (padded_length + 3) * columns)

def print_daily(forecast, tz):

  print_underscore(forecast['daily']['summary'])
  print("")

  data = forecast['daily']['data']
  columns = 5
  padded_length = 30
  
  min = calculate_min(data, lambda item: item['summary'], padded_length - 2, columns)

  def create_values(part, index):
    date = create_date_tz(part['time'], tz)
    (min_f_temp, min_c_temp) = format_temp(part['temperatureLow'])
    (max_f_temp, max_c_temp) = format_temp(part['temperatureHigh'])
    min_date = create_date_tz(part['temperatureLowTime'], tz)
    max_date = create_date_tz(part['apparentTemperatureHighTime'], tz)
    localFormat = "%d %b, %a"

    minutes_format = "%H:%M"
    return [
      date.strftime(localFormat),
      "Min {celcius}°C/{fahrenheit}°F at {date}".format(celcius=min_c_temp, fahrenheit=min_f_temp, date=min_date.strftime(minutes_format)),
      "Max {celcius}°C/{fahrenheit}°F at {date}".format(celcius=max_c_temp, fahrenheit=max_f_temp, date=max_date.strftime(minutes_format)),
      *break_text(part['summary'], padded_length - 2, min=min[index])
    ]

  tables_hourly_values = create_tables(data, create_values,
                                       skip = 1, columns = columns)

  
  for table in tables_hourly_values:
    for row in table:
      str = ""
      for value in row:
        # to make it like a real table, we need to have
        # the same width, so we enforce string length
        str += " {value: <30} |".format(value=value)

      print(str)
    
    # draw a separator after each table
    # 20 for padded value, 2 space, 1 for "|" symbol
    # 6 for number of columns
    print("=" * (padded_length + 3) * columns)

def print_current_weather(forecast):
  current_forecast = forecast['currently']

  # we need to have timezones attached in order to
  # show local time – this is what is important to us
  tz = timezone(forecast['timezone'])
  right_now = render_hourly_part(part = current_forecast, tz=tz)
  
  print(right_now)
  print_today(forecast, tz)
  print("")
  print_daily(forecast, tz)
