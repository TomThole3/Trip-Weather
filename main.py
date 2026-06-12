# -*- coding: utf-8 -*-
from InputOutput import InputOutput
from GPXHandling import GPXHandling
from WeatherAPI import WeatherAPI
from App import Controller
    
def main():
   """
   Main method that starts the application
    
   Returns
   -------
   None.
    
   """
   io = InputOutput()
   gpx_handler = GPXHandling()
   weather_api = WeatherAPI(io)
   con = Controller(io, gpx_handler, weather_api)
   con.app()
    
if __name__ == "__main__":
    main()  
