from .utils import print_underscore, calculate_min, break_text

def render_hourly_part(current_forecast):
  localFormat = "%A, %d %B %Y, %H:%M:%S %z"

  return """{date}
  Right now it is {celcius}°C / {fahrenheit}°F.
  {summary}
  """.format(celcius=current_forecast.c_temp,
             fahrenheit=current_forecast.f_temp,
             summary=current_forecast.summary,
             date=current_forecast.date.strftime(localFormat))

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

def print_today(forecast):
  """
  Print hourly data for the next couple days.
  This function prints several tables with 6 columns max,
  so they don't overflow on the terminal screen.
  """

  print_underscore(forecast.summary)
  print("")

  def create_values(part, index):
    localFormat = "%a %H:%M"

    return [
      part.date.strftime(localFormat),
      "{celcius}°C/{fahrenheit}°F".format(celcius=part.c_temp, fahrenheit=part.f_temp),
      part.summary
    ]

  columns = 6
  tables_hourly_values = create_tables(forecast.parts, create_values,
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

def print_daily(forecast):

  print_underscore(forecast.summary)
  print("")
  
  columns = 5
  padded_length = 30
  
  min = calculate_min(forecast.parts, lambda item: item.summary, padded_length - 2, columns)

  def create_values(part, index):
    localFormat = "%d %b, %a"
    minutes_format = "%H:%M"
    
    return [
      part.date.strftime(localFormat),
      "Min {celcius}°C/{fahrenheit}°F at {date}".format(
        celcius=part.min_c_temp, fahrenheit=part.min_f_temp, date=part.min_date.strftime(minutes_format)),
      "Max {celcius}°C/{fahrenheit}°F at {date}".format(celcius=part.max_c_temp, fahrenheit=part.max_f_temp, date=part.max_date.strftime(minutes_format)),
      *break_text(part.summary, padded_length - 2, min=min[index])
    ]

  tables_hourly_values = create_tables(forecast.parts, create_values,
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
  right_now = render_hourly_part(current_forecast = forecast.get_current_forecast())
  
  print(right_now)
  print_today(forecast.get_hourly_forecast())
  print("")
  print_daily(forecast.get_daily_forecast())