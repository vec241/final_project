__author__ = 'lqo202'
__reviewer__ = 'fnd212'

import Projections
import numpy as np


class ZeroAreaPolygon(Exception):
    pass


def get_density(polygon, ammount):
    """
    This method asumesthat the data inputted is already filtered to be inside the polygon
    Number of crimes per area is calculated as the division of the number of crimes in the zone by the area of the zone
    :param polygon:  a shapely class that represents the limits of the desired zone
    :param ammount: filtered data from the desired zone
    :return: density
    """

    area = Projections.PolygonProjection(polygon).calculate_area_in_miles()
    try:
        density = ammount/area
    except ZeroDivisionError:
        raise ZeroAreaPolygon('Received Polygon has area 0')

    return density


def effectiveness_police(data, key='Arrest'):
    """
    Effectiveness is defined as the number of arrests over the total number of crimes
    :param data
    :return: indicator
    """
    if key not in data.columns:
        raise ValueError('Database does not contain "{}" label to filter.'.format(key))

    try:
        return len(data[data['Arrest'] == True])*1.0 / len(data['Arrest'])
    except ZeroDivisionError:
        return np.nan


def effectiveness_sq_mile(polygon, data, key='Arrest'):
    """ Receives a polygon with the boundaries of the desired zone and lat/lon data.
    Effectiveness by square mile is defined as the number of arrests over a certain area
    :param data
    :param polygon
    :return: effectiveness_sqmile
    """

    if key not in data.columns:
        raise ValueError('Database does not contain "{}" label to filter.'.format(key))

    area = Projections.PolygonProjection(polygon).calculate_area_in_miles()

    try:
        effectiveness_sqmile = effectiveness_police(data, key='Arrest')/area
    except ZeroDivisionError:
        raise ZeroAreaPolygon('Recveived Polygon has area 0')
    
    return effectiveness_sqmile 


