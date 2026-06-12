# -*- coding: utf-8 -*-
import gpxpy
from math import radians, cos, sin, asin, sqrt

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

