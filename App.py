# -*- coding: utf-8 -*-
from datetime import date, timedelta

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
        times, precipitation = self.split_data(data)
        self.io.table(precipitation, times)
        
    def transform_time(self, start_time):
        day, hour, minute = start_time
        actual_date = (date.today() + timedelta(days=day)).day
        minute = (round(minute/15)*15) % 60
        return (actual_date, hour, minute)

    def api_caller(self, coords_list, start_time):
        precipitation = []
        for lat, lon in coords_list:
            full = self.weather_api.get_precipation(lat, lon)
            specific_time = self.weather_api.match_time(full, start_time)
            precipitation.append((specific_time, start_time))
            start_time = self.add_15_minutes(start_time)
        return precipitation
    
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
    
    def split_data(self, data):
        precipitation = [row[0] for row in data]
        times = [f'{timepoint[1]}:{timepoint[2]}' for _, timepoint in data]
        times = [time.replace(':0', ':00') for time in times]
        return times, precipitation

