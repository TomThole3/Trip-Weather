# Trip Weather
When cycling long distances, I always thought it was annoy having to look up the weather for several spots along the way to get an idea of what the weather will be like during the trip. This was the motivation to resolve the issue using the following program.

This project is a python application that turns a .gpx file into a weather forecast. Given the indicated route and a user-defined departure time, it generates a table showing the precipation through the entire trip. This is adjusted for traveling speed, showing the precipation exactly for the locations where the user will be after leaving at the intended starting time. To achieve this, the user's .gpx file is parsed and subsequently the Openmeteo API is called for every location at a 15 minute interval on the route.

## Requirements:
Python 3.10+
gpxpy==1.6.2
matplotlib==3.11.0
openmeteo_requests==1.7.5
pandas==3.0.3

 ## Running the script
 ### GPX file
 Although the most popular online maps do not provide the option to download a route as a .gpx file, several websites exist that do provide this service. Any .gpx file where the route is stored as a track parameter can be used in this program.
 ### The script itself
 With the downloaded requirements, the script can be run in an IDE or from command prompt. While running the script, the user is prompted to provide the path to a valid .gpx file. Then, the user enters their expected traveling speed (in km/h) and starting time. With this information, a plot is shown that contains the precipitation during the trip.

 ## How it works (High level)
 - The user is prompted for the .gpx file, speed and departure time
 - Coordinates are extracted from the .gpx file
 - The distances between the coordinates are calculated
 - An Openmeteo API call is made for every point which is distance-wise 15 minutes from the previous examined point
 - Received precipitation levels throughout the trip are shown in a barplot

 ## Credits
 Code for the Haversine formula was copied from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points.

 ## Limitations
 The first limitation of this program is that it only works within two days of departure, due this constraint with the Openmeteo API for 15-minutely weather predictions. Another theoretical limitation is that the output may be flawed at very long straight stretches, due to the way that these are stored in GPX files. This program is very rare and I was not able to replicate it in practice though. Finally, the program may fail if an incorrect .gpx file is provided, since it is hard to check whether it follows the format before executing it. 
