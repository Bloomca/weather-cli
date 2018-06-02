import datetime

import requests
from pytz import timezone

from .utils import (get_city_coords, format_city,
                    format_temp, create_date_tz)
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
  return Forecast(r.json())

class Forecast:
  def __init__(self, forecast):
    self._data = forecast
    # we need to have timezones attached in order to
    # show local time – this is what is important to us
    self.tz = timezone(forecast['timezone'])

  def get_current_forecast(self):
    return CurrentForecast(self._data['currently'], self.tz)

  def get_hourly_forecast(self):
    return HourlyForecast(self._data['hourly'], self.tz)
  
  def get_daily_forecast(self):
    return DailyForecast(self._data['daily'], self.tz)

class CurrentForecast:
  def __init__(self, current_forecast, tz):
    self.date = create_date_tz(current_forecast['time'], tz)
    self.summary = current_forecast['summary']
    (f_temp, c_temp) = format_temp(current_forecast['temperature'])
    self.f_temp = f_temp
    self.c_temp = c_temp

class FutureForecast:
  def __init__(self, future_forecast, tz):
    self.date = create_date_tz(future_forecast['time'], tz)
    self.min_date = create_date_tz(future_forecast['temperatureLowTime'], tz)
    self.max_date = create_date_tz(future_forecast['apparentTemperatureHighTime'], tz)
    self.summary = future_forecast['summary']

    (min_f_temp, min_c_temp) = format_temp(future_forecast['temperatureLow'])
    (max_f_temp, max_c_temp) = format_temp(future_forecast['temperatureHigh'])
    self.min_f_temp = min_f_temp
    self.min_c_temp = min_c_temp
    self.max_f_temp = max_f_temp
    self.max_c_temp = max_c_temp
    

class HourlyForecast:
  def __init__(self, hourly_forecast_data, tz):
    self.summary = hourly_forecast_data['summary']
    self.parts = list(map(lambda data: CurrentForecast(data, tz), hourly_forecast_data['data']))

class DailyForecast:
  def __init__(self, daily_forecast_data, tz):
    self.summary = daily_forecast_data['summary']
    self.parts = list(map(lambda data: FutureForecast(data, tz), daily_forecast_data['data']))
