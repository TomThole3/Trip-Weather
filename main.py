# -*- coding: utf-8 -*-
import gpxpy
import re
from math import radians, cos, sin, asin, sqrt
import datetime

class Controller:
    
    def __init__(self, io, gpx_handler):
        self.io = io
        self.gpx_handler = gpx_handler
    
    def app(self):
        gpx_path = self.io.get_gpx()
        pace = self.io.get_pace()/4 # 15 minute interval for km/h
        gpx = self.gpx_handler.parse_gpx(gpx_path)
        coords = self.gpx_handler.extract_coords(gpx)
        dist_coords = self.gpx_handler.add_distances(coords)
        stripped = self.gpx_handler.strip_list(dist_coords, pace)

    
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
    

        
    
def main():
   io = InputOutput()
   gpx_handler = GPXHandling()
   con = Controller(io, gpx_handler)
   con.app()
    
if __name__ == "__main__":
    main()  
