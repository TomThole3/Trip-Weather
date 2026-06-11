# -*- coding: utf-8 -*-
import gpxpy
import re
from math import radians, cos, sin, asin, sqrt
import datetime
import openmeteo_requests
import pandas as pd

class Controller:
    
    def __init__(self, io, gpx_handler, weather_api):
        self.io = io
        self.gpx_handler = gpx_handler
        self.weather_api = weather_api
    
    def app(self):
        gpx_path = self.io.get_gpx()
        pace = self.io.get_pace()/4 # 15 minute interval for km/h
        start_time = self.transform_time(self.io.get_start_time())
        gpx = self.gpx_handler.parse_gpx(gpx_path)
        coords = self.gpx_handler.extract_coords(gpx)
        dist_coords = self.gpx_handler.add_distances(coords)
        stripped = self.gpx_handler.strip_list(dist_coords, pace)
        data = self.api_caller(stripped, start_time)
        print(data)
        
    def transform_time(self, start_time):
        day, hour, minute = start_time
        day = datetime.date.day + day
        minute = round(minute/15)*15
        return (day, hour, minute)

    def api_caller(self, coords_list, start_time):
        precipation = []
        for lat, lon in coords_list:
            full = self.weather_api.get_precipation(lat, lon)
            specific_time = self.weather_api.match_time(full, start_time)
            precipation.append((specific_time, start_time))
            start_time = self.add_15_minutes(start_time)
    
    def add_15_minutes(self, time):
        day, hour, minute = time
        minute += 15
        if minute == 60:
            hour += 1
            minute = 0
        if hour == 24:
            day += 1
            hour = 0
        return (day, hour, minute)
    
class InputOutput:
    
    def get_gpx(self):
        while True:
            path = input('Please enter a valid path to a gpx file ')
            if bool(re.search(r'^"?.*\.gpx"?$', path.strip(), re.IGNORECASE)):
                try:
                    path = path.strip('"')
                    open(path, 'r')    
                    return path
                except:
                    print('Invalid path provided')
            else:
                print('No GPX file provided ')
            
    def get_pace(self):
         while True:
             pace = input('At what pace do you think you will be moving in km/h? Enter an integer only ')
             if pace.isdigit():
                 return int(pace)
             print('Please enter a valid integer')
             
    def get_start_time(self):
        while True:
            day = input('Will you leave today (0), tomorrow (1) or the day after tomorrow (2)? ')
            if day.isdigit() and day < 3:
                break
            print('Please enter a valid number')
        while True:
            hour = input("At what hour will you leave? ")
            if hour.isdigit() and hour < 25:
                break
            print('Please enter a valid hour')
        while True:
            minutes = input('At what minute of the given hour will you leave? ')
            if minutes.isdigit() and minutes < 60:
                break
            print('Please enter a valid number of minutes')
        return day, hour, minutes
             
            
class GPXHandling:
    
    def parse_gpx(self, path):
        gpx_file = open(path, 'r')
        return gpxpy.parse(gpx_file)

    def haversine(self, lon1, lat1, lon2, lat2):
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371
        return c * r
    
    def extract_coords(self, gpx):
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        return points
    
    def add_distances(self, points):
        points_dist = []
        points_dist.append((points[0][0], points[0][1], 0))
        for i in range(len(points)-1):
            lat, lon = points[i+1]
            old_lat, old_lon = points[i]
            distance = self.haversine(lat, lon, old_lat, old_lon)
            points_dist.append((lat, lon, distance))
        return points_dist
    
    def strip_list(self, points, pace):
        stripped = []
        stripped.append((points[0][0], points[0][1]))
        count = 0
        for (lat, lon, dist) in points:
            count += dist
            if count > pace:
                stripped.append((lat, lon))
                count -= pace
        return stripped
    
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
    
def main():
   io = InputOutput()
   gpx_handler = GPXHandling()
   weather_api = WeatherAPI()
   con = Controller(io, gpx_handler, weather_api)
   con.app()
    
if __name__ == "__main__":
    main()  
