# -*- coding: utf-8 -*-
import re
import openmeteo_requests
import pandas as pd
import matplotlib.pyplot as plt
    
def main():
    """
    Main method that starts the application
    
    Returns
    -------
    None.
    
    """
   io = InputOutput()
   gpx_handler = GPXHandling()
   weather_api = WeatherAPI()
   con = Controller(io, gpx_handler, weather_api)
   con.app()
    
if __name__ == "__main__":
    main()  
