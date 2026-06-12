# -*- coding: utf-8 -*-
import re
import matplotlib.pyplot as plt

class InputOutput:
    """
    Class concerned with input and output
    """
    
    def get_gpx(self):
        """
        Prompts user for a valid path to a gpx file

        Returns
        -------
        path : Path to a gpx file

        """
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
        """
        Prompts user for their expected speed in km/h

        Returns
        -------
        The pace as an int

        """
        while True:
             pace = input('At what pace do you think you will be moving in km/h? Enter an integer only ')
             if pace.isdigit():
                 return int(pace)
             print('Please enter a valid integer')
             
    def get_start_time(self):
        """
        Prompts user for the time they will start their trip

        Returns
        -------
        Start time as a three integers regarding day, hour and minute

        """
        while True:
            day = input('Will you leave today (0), tomorrow (1) or the day after tomorrow (2)? ')
            if day.isdigit() and int(day) < 3:
                break
            print('Please enter a valid number')
        while True:
            hour = input("At what hour will you leave? ")
            if hour.isdigit() and int(hour) < 25:
                break
            print('Please enter a valid hour')
        while True:
            minutes = input('At what minute of the given hour will you leave? ')
            if minutes.isdigit() and int(minutes) < 60:
                break
            print('Please enter a valid number of minutes')
        return int(day), int(hour), int(minutes)
    
    def table(self, precipitation, times):
        """
        Generates barplot of the precipation

        Parameters
        ----------
        precipitation : List of all precipitation data points
        times : List of all associated timestamps

        Returns
        -------
        None.

        """
        plt.bar(times, precipitation)
        plt.title("Precipitation during your trip ")
        plt.xlabel("Time")
        plt.ylabel("Precipitation")
        
        # Only show every fourth timelabel for clarity
        ax = plt.gca()
        ax.set_xticks(range(0, len(times), 4))
        ax.set_xticklabels(times[::4])
        
        plt.show()
        
    def time_not_found(self, time):
        """
        Error message when queried time is not provided by the openmeteo api

        Parameters
        ----------
        time : First unavailable time

        Returns
        -------
        None.

        """
        print(f'No weather is available after {time}, and values will be unavailable')

