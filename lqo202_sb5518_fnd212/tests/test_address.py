from unittest import TestCase
import addressClass
from addressClass import Address
import googlemaps

class test_database_utils(TestCase):
    
    def setUp(self):
        self.valid_address= '4334 W Washington Blvd, Chicago, IL 60624'
        self.valid_lat_lon = (41.881860, -87.734127)
        self.invalid_address = 'Los maquis 226'

        self.BROKEN_GMAPS_KEY = Address.GMAPS_KEY[:-1] +'0'
        

    def test_address_init(self):
        
        #This part success if address not in Chicago exception is raised
        with self.assertRaises(ValueError):
            address = Address(self.invalid_address)        

        #First part success if no exceptions are raised.   
        address = Address(self.valid_address)

        self.assertAlmostEqual(address.lat, self.valid_lat_lon[0],places=3)
        self.assertAlmostEqual(address.lon, self.valid_lat_lon[1],places=3)
        self.assertAlmostEqual

    def test_wrong_gmaps_key(self):
        
        address = Address(self.valid_address)

        tmp = address.gmaps
        address.gmaps = googlemaps.Client(key=self.BROKEN_GMAPS_KEY)

        with self.assertRaises(addressClass.InvalidGmapsKey):
            address._get_address_info(address.formatted_address)

        address.gmaps = tmp