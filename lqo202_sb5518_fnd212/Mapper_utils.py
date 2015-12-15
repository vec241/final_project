__author__ = 'sb5518'
__reviewer__ = 'lqo202'

from mpl_toolkits.basemap import Basemap
import scipy.ndimage.filters as sc
from matplotlib.colors import BoundaryNorm
from matplotlib.cm import ScalarMappable
import numpy as np
import matplotlib.pyplot as plt
import addressClass as ac
import statistics as sr
import databases_utils as du

"""
This module contains private methods required by the maps_builder class of the Mapper module.
It also contains a custom exception used by the same class.

"""

class MapperError(Exception):
        """
        This class is used to raise errors in the mapper module
        """
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)


def _custom_colorbar(cmap, ncolors, labels, **kwargs):
        """Create a custom, discretized colorbar with correctly formatted/aligned labels.
        It was inspired mostly by the example provided in http://beneathdata.com/how-to/visualizing-my-location-history/

        :param cmap: the matplotlib colormap object you plan on using for your graph
        :param ncolors: (int) the number of discrete colors available
        :param labels: the list of labels for the colorbar. Should be the same length as ncolors.

        :return: custom colorbar
        """

        if ncolors <> len(labels):
            raise MapperError("Number of colors is not compatible with the number of labels")
        else:
            norm = BoundaryNorm(range(0, ncolors), cmap.N)
            mappable = ScalarMappable(cmap=cmap)
            mappable.set_array([])
            mappable.set_clim(-0.5, ncolors+0.5)
            colorbar = plt.colorbar(mappable, **kwargs)
            colorbar.set_ticks(np.linspace(0, ncolors, ncolors+1)+0.5)
            colorbar.set_ticklabels(range(0, ncolors))
            colorbar.set_ticklabels(labels)
            return colorbar


def _steps_labels_for_colorbar_creator(crimes_by_sq):
        """ This function creates a valid step and labels to cleate a custom colorbar object. It is complimentary
        of the _custom_colorbar(cmap, ncolors, labels, **kwargs) function.
        It was inspired mostly by the example provided in http://beneathdata.com/how-to/visualizing-my-location-history/

        :param crimes_by_sq
        :return step, labels
        """
        step = max(crimes_by_sq.values())/len(crimes_by_sq.values())
        # In case the densities are very low, we arbitrarily define step = 1
        if int(step) == 0:
            step = 1

        labels = range(0, int(max(crimes_by_sq.values())), int(step))
        return labels


def _district_mapper_input_validator(crimes, address_object):
        """ This function validates that the input for the district mapper function is correct

        :param crimes: a list or tuple of list or tuple of pairs of coordinates representing crimes
        :param address_object: an instance of the Address class.
        """
        if not (isinstance(crimes, tuple) or isinstance(crimes, list)): # Validates that it is a list or tuple
            raise MapperError("The list provided for crimes is not a list or tuple")

        # Eliminate invalid entries of coordinates that do not belong to Chicago
        invalid_coords_index = []
        for coord in crimes:
            if (not (isinstance(coord, tuple) or isinstance(coord, list))) or (len(coord) != 2):  # Validates that every element in the list has two elements which are supposed to pairs of coordinates
                raise MapperError("At least one element in the list of crimes is not a list or tuple of two elements")
            if not ((coord[0] > 41.62846088888256) and  (coord[0] < 42.042643093713917) or (coord[1] > -87.946463888372286) and  (coord[1] < -87.415897644283177)):   # Valdidates that it is a valid Chicago latitude
                invalid_coords_index.append(crimes.index(coord))

        for invalid in invalid_coords_index:
            crimes.pop(invalid)

        if not isinstance(address_object, ac.Address): # Validates that it is a valid Address class instance
            raise MapperError("The address received is not of the class Address")


def _basemap_district(min_lat, min_lon, max_lat, max_lon):
        """ This function creates a Basemap instance that is a map of a District of chicago

        :param min_lat, min_lon, max_lat, max_lon: integers or floats representing  vertices of the map
        :return district_map
        """
        district_map = Basemap(llcrnrlon=min_lon, llcrnrlat=min_lat, urcrnrlon=max_lon, urcrnrlat=max_lat, projection="merc", resolution = 'h')
        district_map.drawcoastlines()
        district_map.drawcountries()
        district_map.drawcounties()
        district_map.drawmapboundary()
        district_map.drawrivers(color='#0000ff')
        return district_map


def _district_map_limits_calculator(district_number):
        """
        Receives a district Number and returns the coordinates vertices to create a map, the latitudes and longitudes
        lists of the limits of the map and a list of vertices of the map.

        :param district_number:
        :return min_lon, max_lon, min_lat, max_lat, district_limits_lon, district_limits_lat, vertices_list
        """
        if district_number not in du.DISTRICTS: # Validate if the district number is a valid Chicago district
            raise TypeError("District number is not a valid District of Chicago")

        # Save the coordinates of the bounds of the District into 'district_polygon'
        district_polygon = du.get_polygon(district_number)

        # Splits the coordinates into a list of Longitudes and a list of Latitudes
        district_limits_lat = [coordinate[0] for coordinate in district_polygon]
        district_limits_lon = [coordinate[1] for coordinate in district_polygon]

        # Create limits of the map to be slightly bigger than the limits of the district.
        min_lon = min(district_limits_lon) - 0.002
        max_lon = max(district_limits_lon) + 0.002
        min_lat = min(district_limits_lat) - 0.002
        max_lat = max(district_limits_lat) + 0.002

        # Create a list of the new vertices of the map
        vertices_list = [(min_lat, min_lon), (max_lat, min_lon), (max_lat, max_lon), (min_lat, max_lon)]

        return min_lon, max_lon, min_lat, max_lat, district_limits_lon, district_limits_lat, vertices_list


def _crimes_lon_lat_splitter(filtered_crimes):
        """
        Receives a list or tuple of lists or tuples representing latitude-longitude pairs and split the latitudes and
        longitudes into two separate lists.

        :param filtered_crimes:
        :return lat_list, lon_list
        """
        lon_list = [coordinate[1] for coordinate in filtered_crimes]
        lat_list = [coordinate[0] for coordinate in filtered_crimes]
        return lat_list, lon_list


def _bin_densities_calculator(lat_list, lon_list):
        """
        Receives two lists representing latitudes and longitudes and returns binned latitudes and longitudes and
        a smoothed density grid

        :param lat_list, lon_list
        :return lat_bins_2d, lon_bins_2d, smoothed_density
        """
        # In case they are empty lists, meaning there are no crimes for the selected crime type and year, we arbitrarily
        #  define the max and min latitudes and longitudes as 0
        if len(lat_list) == 0 or len(lon_list) == 0:
            lon_max, lon_min, lat_max, lat_min = 0, 0, 0, 0
        # Get the maximum and minimum values of the latitudes and longitudes lists of crimes.
        else:
            lon_max, lon_min, lat_max, lat_min = max(lon_list), min(lon_list), max(lat_list), min(lat_list)

        # Compute appropriate bins to chop up the data in order to draw HeatMap:
        db = 0.001 # bin padding

        lon_bins = np.linspace(lon_min-db, lon_max+db, 60+1) # 10 bins
        lat_bins = np.linspace(lat_min-db, lat_max+db, 66+1) # 13 bins

        # Compute the density of crimes by bin
        density, _, _ = np.histogram2d(lon_list, lat_list, [lon_bins, lat_bins])

        # Smooth the density with a gaussian filter
        smoothed_density = sc.gaussian_filter(density, 2.5)

        # Turn the lon/lat of the bins into 2 dimensional arrays ready
        # for conversion into projected coordinates
        lat_bins_2d, lon_bins_2d = np.meshgrid(lat_bins, lon_bins)

        return lat_bins_2d, lon_bins_2d, smoothed_density


def _city_mapper_validator(crimes_by_sq):

        """
        Validates that the object is a dictionary with keys representing valid chicago district numbers and values
        representing valid crime densities.

        If there are no values for some valid districts, meaning there were no crimes in that district, an entry with
        value 0 will be created.

        :param crimes_by_sq
        """
        if not isinstance(crimes_by_sq, dict):
            raise TypeError("City Mapper method was not provided with a dictionary")

        for possible_district in crimes_by_sq.keys():  # Validate that the keys from the dictionary are valid districts
            if (possible_district not in du.DISTRICTS):
                raise TypeError("At least one of the elements of the dictionary does not correspond to a valid district ({})".format(possible_district))

        for possible_density in crimes_by_sq.values(): # Validate that the values of the dictionary are numbers
            if not (isinstance(possible_density, int) or isinstance(possible_density, float)):
                raise TypeError("At least one of the elements of the dictionary is not a number and though not possibly a density")

        if len(crimes_by_sq.keys()) < len(du.DISTRICTS):
            for district in du.DISTRICTS:
                if district not in crimes_by_sq.keys():
                    crimes_by_sq[district] = 0

        return crimes_by_sq

def _basemap_city():
        """
        This function creates a Basemap instance that is a map of Chicago with its districts

        :return city_map
        """
        city_map = Basemap(llcrnrlon=-87.946463888372286, llcrnrlat=41.62846088888256, urcrnrlon=-87.415897644283177, urcrnrlat=42.042643093713917, projection="merc", resolution = 'h')
        city_map.drawcoastlines()
        city_map.drawmapboundary(fill_color='#99ffff')
        city_map.fillcontinents(color='#804000', lake_color='#009799')
        city_map.drawrivers(color='b')
        city_map.readshapefile('./Databases/districts/geo_fthy-xz3r-1', 'district_m')

        # Label Lake michigan
        lat_lake, lon_lake = 42.008124, -87.567399
        x_lake, y_lake = city_map(lon_lake, lat_lake)
        plt.text(x_lake, y_lake, 'Lake Michigan', fontsize=10, fontweight='bold', va='bottom', ha='center', color='k')
        return city_map


def _address_object_list_validator(address_list):
        """
        This function validates it the object received is a list or tuple of instances of Address class

        :param address_list
        """
        if not (isinstance(address_list, list) or isinstance(address_list, tuple)):
            raise TypeError("Address list is not a list or tuple")
        for address_object in address_list:
            if not isinstance(address_object, ac.Address):
                raise TypeError("At least one object of the address list is not an Address object")


def _crime_dataframe_validator(crimes_base):
        """
        This function validates it the object received is an instance of CrimesDataFrame class

        :param crimes_base
        """
        if not isinstance(crimes_base, sr.CrimesDataFrame):
            raise TypeError("City mapper requires a CrimeDataframe object")