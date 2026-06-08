# -*- coding: utf-8 -*-
import gpxpy
import re

class Controller:
    
    def __init__(self, io):
        self.io = io
    
    def app(self):
        gpx_path = self.io.get_gpx()
    
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
            
class GPXHandling:
    def __init__(self, path):
        self.path = path
            

def main():
   io = InputOutput()
   con = Controller(io)
   con.app()
    
if __name__ == "__main__":
    main()  

