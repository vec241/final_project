from unittest import TestCase
import databases_utils

class test_database_utils(TestCase):

    def setUp(self):
        self.valid_districts= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22, 24, 25]
        self.invalid_districts = [35,50,100]
        self.malformed_districts = [[1,2,3],(1,4)]
        self.district = 8

        self.lat_lon_district_11 = (41.881860, -87.734127)
        self.lat_lon_not_in_chicago = (100.0, 100.0)


    def test_get_polygon_valid_inputs(self):
        ''' This test will pass if no exceptions are raised '''
        for district in self.valid_districts:
            databases_utils.get_polygon(district)

    def test_get_polygon_invalid_inputs(self):
        for district in self.invalid_districts:
            with self.assertRaises(ValueError):
                databases_utils.get_polygon(district)

        for district in self.malformed_districts:
            with self.assertRaises(TypeError):
                databases_utils.get_polygon(district)


    def test_police_station_coordinates(self):
        #This part of the test will pass if no exceptions are raised
        for district in self.valid_districts:
            databases_utils.get_police_station_coordinates(district)

        #This part of the test will pass if ValueError exception is raised
        for district in self.invalid_districts:
            with self.assertRaises(ValueError):
                databases_utils.get_police_station_coordinates(district)

        for district in self.malformed_districts:
            with self.assertRaises(TypeError):
                databases_utils.get_police_station_coordinates(district)

    def test_try_open_wrong_DB(self):
        with self.assertRaises(IOError):
            databases_utils.get_police_station_coordinates(self.valid_districts[0],db_police='xxx')



    def test_get_district_from_lat_lon(self):

        self.assertEqual(databases_utils.get_district_from_lat_lon(self.lat_lon_district_11) , 11)

        with self.assertRaises(ValueError):
            databases_utils.get_district_from_lat_lon(self.lat_lon_not_in_chicago)


