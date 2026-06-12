# -*- coding: utf-8 -*-
import openmeteo_requests
import pandas as pd

class WeatherAPI:
    def __init__(self):
        self.client = openmeteo_requests.Client()
    
    
    def get_precipation(self, lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
        	"latitude": lat,
        	"longitude": lon,
        	"minutely_15": ["precipitation"],
            "timezone": "Europe/Berlin",
        }
        responses = self.client.weather_api(url, params=params)
        response = responses[0]

        minutely_15 = response.Minutely15()
        minutely_15_precipitation = minutely_15.Variables(0).ValuesAsNumpy()

        minutely_15_data = {
        	"date": pd.date_range(
        		start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
        		end =  pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
        		freq = pd.Timedelta(seconds = minutely_15.Interval()),
        		inclusive = "left"
        	)
        }

        minutely_15_data["precipitation"] = minutely_15_precipitation
        data = list(zip(minutely_15_precipitation, minutely_15_data['date']))
        transformed = dict([((stamp.day, stamp.hour, stamp.minute), float(precipitation)) for (precipitation, stamp) in data])

        return transformed
    
    def match_time(self, data, time): 
        return data[time]

