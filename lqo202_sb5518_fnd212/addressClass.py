__author__ = 'fnd212'
__reviewer__ = 'sb5518'

"""
This module contains an exception to represent a NoInternetAccess exception
and the class Address which is used to represent a Chicago Address.
"""

import googlemaps
from databases_utils import get_district_from_lat_lon, get_police_station_coordinates
from defined_exceptions import QuitProgram
import googlemaps.exceptions as gmaps_exceptions
from geometry_utils import calculate_distance_between_points
import sys

def is_internet_on():
    """Checks internet connectivity, returns boolean.
    :return boolean
    """
    try:
        response = urlopen('http://google.com',timeout=5)
        return True
    except:
        return False

class NoInternetAccess(Exception):
    pass
class NotGmapsKey(Exception):
    pass
class InvalidGmapsKey(Exception): 
    pass


class Address(object):
    """
    Class to represent an address.
    Class Atributes:
        - GMAPS_KEY: stores the key for gmaps API.
        - gmaps: gmap client.

    Methods:
        - get_address(self)

    Instance Attributes:
        - lat:  Latitude of the Address
        - lon:  Longitude of the Address
        - formatted_address: Full String Representing the Address
        - district: The District Number where the address is located
        - street_address: String representing only the Street Address
        - distance_to_police_station
        - summary: statistics.AddressStatistics object.
    """


    GMAPS_KEY_FILE = './gmapskey.key'
    try:
        GMAPS_KEY = open(GMAPS_KEY_FILE).read()
        gmaps = googlemaps.Client(key=GMAPS_KEY)
    except IOError:
        print ('Fatal Error: Not gmaps key found in {}'.format(GMAPS_KEY_FILE))
        sys.exit(1)
    except ValueError:
        print('Fatal Error: gmaps API Key in {} is invalid'.format(GMAPS_KEY_FILE))
        sys.exit(1)



    def _get_address_info(self, address):
        """
        Uses gmaps API to retrieve the information about the address.
        :param address
        """
        try:
            geocode_result = self.gmaps.geocode(address)
        # Raises gmaps_exceptions.TransportError if no internet addresss.
        except gmaps_exceptions.TransportError:
            raise NoInternetAccess()
        except gmaps_exceptions.ApiError: 
            raise InvalidGmapsKey('Key in {} is an invalid gmaps API key'.format(self.GMAPS_KEY_FILE))

        self.address_info = geocode_result[0]

    def _is_in_chicago(self,user_address):
        """
        Checks if the address passed in string type is in Chicago.
        :param user_address
        :return boolean
        """
        if not isinstance(user_address, str):
            return False

        if 'Chicago' not in user_address:
            user_address = user_address + ', Chicago, IL, USA'

        self._get_address_info(user_address)

        try:
            get_district_from_lat_lon(self._get_address_lat_lon())
        except ValueError:
            return False

        if self.address_info['formatted_address'] == 'Chicago, IL, USA':
            return False

        return True



    def get_address(self):
        """
        Asks the user for an address, validates that it is in Chicago
        and saves
        """

        while 1:
            try:
                user_address = raw_input('Please enter an address in Chicago or [Q]uit: ')
            except EOFError:
                #Do nothing and ask for an address again.
                pass
            else:
                if user_address == 'Q':
                    raise QuitProgram
                if self._is_in_chicago(user_address):
                    #If address_info is empty, then ask again for an address.
                    break

            print('Address not found in Chicago, please try again or [Q]uit')



    def _get_address_lat_lon(self):
        """
        Saves the lat and lon of the address in their corresponding attributes.
        :return (lat, lon)
        """
        lat = self.address_info['geometry']['location']['lat']
        lon = self.address_info['geometry']['location']['lng']

        return (lat,lon)

    def _get_street_address(self):
        """
        Generates the address string from self.formatted_address.
        :return addres_string
        """
        address_parts = self.formatted_address.split(",")
        del address_parts[-3:]
        address_string = ' '.join(address_parts)
        return address_string

    def __eq__(self,other):
        """
        Two objects are considered equal if their formatted_address is the same.
        """
        if self.formatted_address == other.formatted_address:
            return True
        else:
            return False

    def __ne__(self,other):
        if not self.__eq__(self,other):
            return True
        else:
            return False

    def __init__(self, address = None):

        if address:
            if not self._is_in_chicago(address):
                raise ValueError('Address not in Chicago')

        else:
            self.get_address()

        self.formatted_address = self.address_info['formatted_address']
        self.lat,self.lon = self._get_address_lat_lon()
        self.district = get_district_from_lat_lon((self.lat,self.lon))
        self.street_address = self._get_street_address()

        police_station_lat, police_station_lon  = get_police_station_coordinates(self.district)
        self.distance_to_police_station = calculate_distance_between_points(self.lat,self.lon, police_station_lat, police_station_lon)

        self.summary = None



