# -*- coding: utf-8 -*-
import gpxpy
from math import radians, cos, sin, asin, sqrt

class GPXHandling:
    """
    Class concerned with extracting and transforming data of GPX files
    """
    
    def parse_gpx(self, path):
        """
        Parameters
        ----------
        path : Path of gpx file

        Returns
        -------
        parsed gpx file

        """
        gpx_file = open(path, 'r')
        return gpxpy.parse(gpx_file)

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Formula to calculate distance between two coordinates. 
        Taken from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

        Parameters
        ----------
        lon1 : First longitude point
        lat1 : First latitude point
        lon2 : Second longitude point
        lat2 : Second latitude point

        Returns
        -------
        Distance between two coordinates

        """
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
        """
        Extracts coordinates from all points of the route of a gpx file

        Parameters
        ----------
        gpx : Parsed gpx file

        Returns
        -------
        points : List of all points of the route

        """
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        return points
    
    def add_distances(self, points):
        """
        Extends a list of points by turning points into a tuple of the point
        and the distance between point n and point n+1

        Parameters
        ----------
        points : list of points (coordinates)

        Returns
        -------
        points_dist : list of tuples of points and distances

        """
        points_dist = []
        points_dist.append((points[0][0], points[0][1], 0))
        for i in range(len(points)-1):
            lat, lon = points[i+1]
            old_lat, old_lon = points[i]
            distance = self.haversine(lat, lon, old_lat, old_lon)
            points_dist.append((lat, lon, distance))
        return points_dist
    
    def strip_list(self, points, pace):
        """
        Cuts list points keeping only the points that are reached
        every 15 minutes with the given speed

        Parameters
        ----------
        points : List of points (coordinates)
        pace : Pace with which is travelled

        Returns
        -------
        stripped : List containing only points reached at 15 minute marks

        """
        stripped = []
        stripped.append((points[0][0], points[0][1]))
        count = 0
        for (lat, lon, dist) in points:
            count += dist
            if count > pace:
                stripped.append((lat, lon))
                count -= pace
        return stripped

