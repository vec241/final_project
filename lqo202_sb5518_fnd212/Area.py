__author__ = 'lqo202'
__reviewer__ = 'fnd212'

from numpy import pi, cos, radians


class AreaCalculations:

    def __init__(self, polygon):

        latitude = []
        longitude = []
        if isinstance(polygon, list):
            for i in range(len(polygon)):
                latitude.append(polygon[i][1])
                longitude.append(polygon[i][0])
            self.latitude_points = latitude
            self.longitude_points = longitude
        else:
            raise TypeError("Object is not a a list of coordinates!")


    def __reproject(self):

        """
        Returns the x & y coordinates using a sinusoidal projection
        :return x, y
        """
        latitude = self.latitude_points
        longitude = self.longitude_points
        earth_radius = 3963 # in miles
        lat_dist = pi * earth_radius / 180.0
        y = [lat * lat_dist for lat in latitude]
        x = [long * lat_dist * cos(radians(lat)) for lat, long in zip(latitude, longitude)]
        return x, y

    def calculate_area_in_miles(self):
        """Calculates the area of an arbitrary polygon given its vertices
        """
        try:
            x, y = self.__reproject()
        except ValueError:
            raise  ValueError("Inputs are not numbers, Define again with a list containing numbers")
        else:
            area = 0.0
            for i in xrange(-1, len(x)-1):
                area += x[i] * (y[i+1] - y[i-1])
            return abs(area) / 2.0


