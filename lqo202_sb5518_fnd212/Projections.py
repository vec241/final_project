__author__ = 'lqo202'
__reviewer__ = 'fnd212'


from numpy import pi, cos, radians


class PolygonProjection:

    def __init__(self, polygon):
        """
        :param polygon: a list of coordinates lat long, generally obtained from get_polygon in utils functions
        :return latitude_points, longitude_points
        """
        if not isinstance(polygon, list):
            raise TypeError("Object is not a a list of coordinates!")

        for point in polygon:
            if not (isinstance(point,list) or isinstance(point,tuple)):
                raise TypeError('Values in coordinates should be lists or tuples of coordinates')
            if len(point) != 2:
                raise ValueError('Each coordinate should be represented as a list or tuple of two values, lat and lon')

        self.latitude_points = [lonlat[0] for lonlat in polygon]
        self.longitude_points = [lonlat[1] for lonlat in polygon] 

    def _reproject(self):
        """
        Returns the x & y coordinates using a sinusoidal projection
        :return x, y
        """
        earth_radius = 3963 # in miles
        lat_dist = pi * earth_radius / 180.0

        y = [lat * lat_dist for lat in self.latitude_points]
        x = [long * lat_dist * cos(radians(lat)) for lat, long in 
                zip(self.latitude_points, self.longitude_points)]
        
        return x, y

    def calculate_area_in_miles(self):
        """Calculates the area of an arbitrary polygon given its vertices"""
        try:
            x, y = self._reproject()
        except ValueError:
            raise  ValueError('Malformed object. Latitude and longitude points must be arrays of numbers')
        else:
            area = 0.0
            for i in xrange(-1, len(x)-1):
                area += x[i] * (y[i+1] - y[i-1])
            return abs(area) / 2.0


