__author__ = 'lqo202'
__reviewer__ = 'fnd212'

from shapely.geometry import Point, Polygon
from numpy import radians, sin, cos, arctan2, sqrt

def return_points_in_polygon(coordinates, polygon_boundaries):
    """
    Receives a list of tuples of coordinates and returns those
    tuples that are contained within the boundaries of the polygon
    specified in polygon_boundaries
    :param coordinates
    :param polygon_boundaries
    :return contained_points
    """

    #Verify that the inputs of the function are correct.
    if not (isinstance(coordinates,list) and isinstance(polygon_boundaries,list)):
        raise TypeError('List of tuples of coordinates is expected for coordinates and polygon_boundaries')

    for point in coordinates:
        if not (isinstance(point,list) or isinstance(point,tuple)):
            raise TypeError('Values in coordinates should be lists or tuples of coordinates')
        if len(point) != 2:
            raise ValueError('Each coordinate should be represented as a list or tuple of two values, lat and lon')

    for boundary_point in polygon_boundaries:
        if not (isinstance(boundary_point,list) or isinstance(boundary_point,tuple)):
            raise TypeError('Values in coordinates should be lists or tuples of coordinates')
        if len(boundary_point) != 2:
            raise ValueError('Each coordinate should be represented as a list or tuple of two values, lat and lon')

    polygon = Polygon(polygon_boundaries)
    contained_points = list()

    for point in coordinates:
        if polygon.contains(Point(point)):
            contained_points.append(point)

    return contained_points


def return_points_in_square(coordinates, lat_min, lat_max, lon_min, lon_max):
    """
    Receives the latitude/longitude vertices of a series of latitude/longitude
    points. Returns only the points inside the square.

    :param coordinates:
    :param lat_min:
    :param lat_max:
    :param lon_min:
    :param lon_max:
    """
    # Verify that the inputs of the function are correct.
    if not isinstance(coordinates,list):
        raise TypeError('List of tuples of coordinates is expected for coordinates')

    for point in coordinates:
        if not (isinstance(point,list) or isinstance(point,tuple)):
            raise TypeError('Values in coordinates should be lists or tuples of coordinates')
        if len(point) != 2:
            raise ValueError('Each coordinate should be represented as a list or tuple of two values, lat and lon')

    if lat_min > lat_max:
        raise ValueError('lat_min should be less or equal than lat_max')
    if lat_max < lat_min:
        raise ValueError('lat_max should be greater or equal than lat_min')
    if lon_min > lon_max:
        raise ValueError('lon_min should be less or equal than lon_max')
    if lon_max < lon_min:
        raise ValueError('lon_max should be greater or equal than lon_min')

    contained_points = list()
    for point in coordinates:
        if point[0]>lat_min and point[0]<lat_max and point[1]>lon_min and point[1]<lon_max:
            contained_points.append(point)

    return contained_points


def calculate_distance_between_points(lat1, long1, lat2, long2):
        """
        This function is done considering the calculation in the Haversine Formula
        It returns the distance betweeen the given coordinates in miles.
        :param lat1, long1, lat2, long2
        :return distance
        """

        # Radio of the earth in miles
        R = 3963
        # Getting difference and transforming to radians
        dLat = radians(lat1-lat2)
        dLong = radians(long1-long2)

        # Computing with Haversine
        var_a = sin(dLat / 2) * sin(dLat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLong / 2) * sin(dLong / 2)
        var_c = 2 * arctan2(sqrt(var_a),sqrt(1 - var_a))
        distance = R * var_c

        return distance