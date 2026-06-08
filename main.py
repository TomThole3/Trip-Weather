# -*- coding: utf-8 -*-
import gpxpy
import re
from math import radians, cos, sin, asin, sqrt

class Controller:
    
    def __init__(self, io):
        self.io = io
    
    def app(self):
        gpx_path = self.io.get_gpx()
        pace = self.io.get_pace()
    
class InputOutput:
    def get_gpx(self):
        while True:
            path = input('Please enter a valid path to a gpx file ')
            if bool(re.search(r'\.gpx$', path, re.IGNORECASE)):
                try:
                    open(path)    
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
             
            
class GPXHandling:
    def __init__(self, path):
        self.gpx = self.parse_gpx(path)
        
    def parse_gpx(path):
        gpx_file = open(r'C:\Users\tthol\Downloads\mapstogpx20260608_062451.gpx', 'r')
        return gpxpy.parse(gpx_file)
        
    def pace_to_distance(self, pace):
        return pace/4

    def haversine(lon1, lat1, lon2, lat2):
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371
        return c * r

        
            

def main():
   io = InputOutput()
   con = Controller(io)
   con.app()
    
if __name__ == "__main__":
    main()  

