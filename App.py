# -*- coding: utf-8 -*-
from datetime import date, timedelta

class Controller:
    """
    Class containing the main control function and various helper functions
    """
    
    def __init__(self, io, gpx_handler, weather_api):
        """
        Parameters
        ----------
        io : Instance of InputOutput class
        gpx_handler : Instance of GPXHandling class
        weather_api : Instance of WeatherAPI class

        Returns
        -------
        None.

        """
        self.io = io
        self.gpx_handler = gpx_handler
        self.weather_api = weather_api
    
    def app(self):
        """
        Main controller operating and directing functions of the different classes

        Returns
        -------
        None.

        """
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
        """
        Processes time from tuple of relative date, hour and minute
        to absolute day, hour and closest multiple of 15 minutes

        Parameters
        ----------
        start_time : Original tuple of relative date, hour and minute

        Returns
        -------
        actual_date : Date of the trip
        hour : Departure hour of the trip
        minute : Closest 15 minute mark

        """
        day, hour, minute = start_time
        actual_date = (date.today() + timedelta(days=day)).day
        minute = (round(minute/15)*15) % 60
        return (actual_date, hour, minute)

    def api_caller(self, coords_list, start_time):
        """
        Helper function that calls WeatherAPI for each coordinate and filters
        for value at specific time

        Parameters
        ----------
        coords_list : List of coordinates for which weather is requested
        start_time : First timepoint

        Returns
        -------
        precipitation : List of precipitation values at increasing timestamps
        along the route

        """
        precipitation = []
        for lat, lon in coords_list:
            full = self.weather_api.get_precipation(lat, lon)
            specific_time = self.weather_api.match_time(full, start_time)
            if specific_time == -1:
                break
            precipitation.append((specific_time, start_time))
            start_time = self.add_15_minutes(start_time)
        return precipitation
    
    def add_15_minutes(self, time):
        """
        Increases timestamp by 15 minutes

        Parameters
        ----------
        time : Original timestamp

        Returns
        -------
        day : Day of the timestamp
        hour : Hour of the timestamp
        minute : minute of the timestamp

        """
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
        """
        Splits weatherdata into seperate lists of precipitation and time data

        Parameters
        ----------
        data : Original combined weather data

        Returns
        -------
        times : List of times
        precipitation : List of precipitation values

        """
        precipitation = [row[0] for row in data]
        times = [f'{timepoint[1]}:{timepoint[2]}' for _, timepoint in data]
        times = [time.replace(':0', ':00') for time in times]
        return times, precipitation

