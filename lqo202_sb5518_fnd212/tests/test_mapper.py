__author__ = 'sb5518'
__reviewer__ = 'lqo202'

from unittest import TestCase
import Mapper
import Mapper_utils as mu
import addressClass as ac
import pandas as pd
import statistics as sr


class Test_Mapper(TestCase):
    def setUp(self):
        self.db = pd.read_csv('csv_for_test.csv')
        self.valid_crime_coordinates_district_11 = zip(self.db.Latitude, self.db.Longitude)

        self.invalid_crime_coordinates_1 = 1.5
        self.invalid_crime_coordinates_2 = [(41.877788947, -87.723131375), (41.8729007)]

        self.valid_address_object1 = ac.Address('4136 W Adams St')
        self.valid_address_object2 = ac.Address('7628 S St Lawrence Ave')

        self.valid_address_list = (self.valid_address_object1, self.valid_address_object2)

        self.invalid_address_list1 = 1
        self.invalid_address_list2 = (self.valid_address_object1, self.valid_address_object2, "address")

        self.invalid_address_object1 = 1
        self.invalid_address_object2 = list()

        self.valid_crimes_base = sr.CrimesDataFrame(pd.read_csv('csv_for_test.csv'))
        self.invalid_crimes_base = 1

        self.valid_crime_density_by_district_1 = {1: 1, 2: 4, 3: 9, 4: 16.3, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81.788, 10: 100, 11: 121, 12: 144.323, 14: 196, 15: 225, 16: 256, 17: 289, 18: 324, 19: 361, 20: 3, 22: 0, 24: 600, 25: 625}
        self.invalid_crime_density_by_district_1 = 1

    def test_district_mapper_invalid_crimes(self):
        with self.assertRaises(mu.MapperError):
            Mapper.maps_builder.district_mapper(self.invalid_crime_coordinates_1, self.valid_address_object1)

    def test_district_mapper_invalid_crimes2(self):
        with self.assertRaises(mu.MapperError):
            Mapper.maps_builder.district_mapper(self.invalid_crime_coordinates_2, self.valid_address_object2)

    def test_district_mapper_invalid_address1(self):
        with self.assertRaises(mu.MapperError):
            Mapper.maps_builder.district_mapper(self.valid_crime_coordinates_district_11, self.invalid_address_object1)

    def test_district_mapper_invalid_address2(self):
        with self.assertRaises(mu.MapperError):
            Mapper.maps_builder.district_mapper(self.valid_crime_coordinates_district_11, self.invalid_address_object2)

    def test_district_mapper_invalid_address3(self):
        with self.assertRaises(ValueError):
            Mapper.maps_builder.district_mapper(self.valid_crime_coordinates_district_11, ac.Address('fasdfasdfasf'))

    def test_district_mapper_valid(self):
        Mapper.maps_builder.district_mapper(self.valid_crime_coordinates_district_11, self.valid_address_object1, False)

    def test_city_mapper_invalid_address_list1(self):
        with self.assertRaises(TypeError):
            Mapper.maps_builder.city_mapper(self.valid_crimes_base, self.invalid_address_list1)

    def test_city_mapper_invalid_address_list2(self):
        with self.assertRaises(TypeError):
            Mapper.maps_builder.city_mapper(self.valid_crimes_base, self.invalid_address_list2)

    def test_city_mapper_invalid_crimes_base(self):
        with self.assertRaises(TypeError):
            Mapper.maps_builder.city_mapper(self.invalid_crimes_base, self.valid_address_list)

    def test_city_mapper_valid(self):
        Mapper.maps_builder.city_mapper(self.valid_crimes_base, self.valid_address_list, False)

    def test_district_map_limits_calculator(self):
        with self.assertRaises(TypeError):
            mu._district_map_limits_calculator(23)


