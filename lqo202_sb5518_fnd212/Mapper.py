__author__ = 'sb5518'
__reviewer__ = 'lqo202'

import matplotlib.pyplot as plt
import databases_utils
from matplotlib.collections import PatchCollection
from matplotlib import cm
import numpy as np
import geometry_utils as gu
from matplotlib.patches import Polygon
import Mapper_utils as mu

"""
This module contains the maps_builder class, which basically has two public functions to create and show crime maps

* district_mapper method receives a list of tuples of list of tuples that represent pairs of latitudes/longitudes. These
latitudes longitudes are crimes that occurred in the city of Chicago. It also receives an Address object which represent
an Address of the city of Chicago. It creates a custom HeatMap to visualize the district where the Address is and show
the level of crime rate in the different areas around this Address, as well as the respective Police Station.

* city_mapper method receives an instance of CrimesDataFrame and a list or tuple of instances of the Address class.
It basically shows a Heat Map of Chicago with every District and how the different districts are compared in terms of
Crime density. It shows the different addresses of the list in the map as well.

Most of the private functions required for this class to work are located in the Mapper_utils module.

Some parts of the code found inspiration in the following examples:

# The Heat Map of the district is inspired in the following example: http://bagrow.com/dsv/heatmap_basemap.html
# The _custom_colorbar used for the city_mapper was inspired in the code provided in: http://beneathdata.com/how-to/visualizing-my-location-history/

Thank you very much for posting such inspiring examples!
"""


class maps_builder:

        @staticmethod
        def district_mapper(crimes, address_object, show_district_block=True):
                """Create and shows a Custom Heat map of a particular district of Chicago city. Heat will be based on crime density,
                and each individual crime will be a translucent blue point. Police station will be plotted as a violet
                point, and the particular address as a black point.

                Several parts of the code on how to create a Heat map, where inspired by the example found in
                http://bagrow.com/dsv/heatmap_basemap.html. However, they were highly customized and modified for our
                particular use case.

                :param crimes: list or tuple of lists or tuples of coordinates for crimes.
                :param address_object: Receives an instance of the Address class from the addressClass module
                """

                # Validate input
                mu._district_mapper_input_validator(crimes, address_object)

                # Get the district number, longitude and latitude of the address of interest, and string representation of the street address.
                district_number, lat_address, lon_address, street_address = address_object.district, address_object.lat, address_object.lon, address_object.street_address

                # Get proper limits for the district and create limits for the map based on the maximum and minimum latitudes of the district plus a certain margin.
                min_lon, max_lon, min_lat, max_lat, district_limits_lon, district_limits_lat, vertices_list = mu._district_map_limits_calculator(district_number)

                # Filter the crimes database to keep only crimes inside the map space.
                filtered_crimes = gu.return_points_in_square(crimes, min_lat, max_lat, min_lon, max_lon)

                # Save the coordinates of the crimes to plot in two lists.
                lat_crimes_list, lon_crimes_list = mu._crimes_lon_lat_splitter(filtered_crimes)

                plt.close('all')

                # Create a basemap instance of the district with the limits that were established before.
                district_map = mu._basemap_district(min_lat, min_lon, max_lat, max_lon)

                # Generate bins for the Heatmap, calculate densities and smooth densities
                lat_bins_2d, lon_bins_2d, smoothed_density = mu._bin_densities_calculator(lat_crimes_list, lon_crimes_list)

                # Convert the bin mesh to map coordinates:
                xs, ys = district_map(lon_bins_2d, lat_bins_2d)

                # Add histogram squares and a corresponding colorbar to the map:
                plt.pcolormesh(xs, ys, smoothed_density, cmap=cm.OrRd)


                # Add colorbar into the map
                cbar = plt.colorbar(orientation='horizontal', shrink=0.625, aspect=20, fraction=0.2, pad=0.02)
                cbar.set_label('Number of crimes in district number ' + str(district_number), size=18)


                # Translucent blue scatter plot of Crimes above histogram:
                x_crimes, y_crimes = district_map(lon_crimes_list, lat_crimes_list)
                district_map.plot(x_crimes, y_crimes, 'o', markersize=1, zorder=6, markerfacecolor='#424FA4', markeredgecolor="none", alpha=0.33)

                # Get the coordinates of the Police Station of the District and plot it.
                police_coordinates = databases_utils.get_police_station_coordinates(district_number)
                x_police, y_police = district_map(police_coordinates[1], police_coordinates[0])

                district_map.plot(x_police, y_police, marker='D', color='m')
                plt.annotate('Police Station', xy=(x_police, y_police), xycoords='data', xytext=(district_map(police_coordinates[1]+0.001, police_coordinates[0]+0.001)), textcoords='data', color='m')

                # Get the coordinates of the address and plot it
                x_address, y_address = district_map(lon_address, lat_address)

                district_map.plot(x_address, y_address, marker='D', color='#7FFF00')

                plt.annotate(street_address, xy=(x_address, y_address), xycoords='data', xytext=(district_map(lon_address + 0.001, lat_address + 0.001)), textcoords='data', color='k')

                # Plot the boundaries of the Districts
                district_map.readshapefile('./Databases/districts/geo_fthy-xz3r-1', 'district_m')

                # Highlight the boundaries of our District of interest with black.
                ds_1, ds_2 = district_map(district_limits_lon, district_limits_lat)
                district_map.plot(ds_1, ds_2, linewidth=2, color='#000000')

                # Set the size of the image and show the plot
                plt.gcf().set_size_inches(15, 15)
                plt.show(block=show_district_block)


        @staticmethod
        def city_mapper(crimes_base, address_list, show_city_block=True):

                """Create a custom map of Chicago city with its districts. The color of each district will be determined
                by the relative ammount of crimes by square mile of that district. Police stations will be plotted as a
                violet points.

                :param crimes_base a CrimesDataFrame instance
                :param address_list a list of instances of addressClass
                """

                # Validate the crimes_base input
                mu._crime_dataframe_validator(crimes_base)

                # Validate the address_list input
                mu._address_object_list_validator(address_list)

                # Get the crime density by district
                crimes_by_sq_tentative = crimes_base.crime_density_by_district()

                # Validate that the output is correct, which should be a Dictionary with the valid districts as keys and densities represented by numbers as values
                crimes_by_sq = mu._city_mapper_validator(crimes_by_sq_tentative)

                # Create a colormap to show safer areas with blue and dangerous areas with red.
                cmap = plt.get_cmap('RdYlBu_r', int(max(crimes_by_sq.values())))

                # Create equally spaced labels for a color bar.
                labels = mu._steps_labels_for_colorbar_creator(crimes_by_sq)

                # Start plotting the figure
                plt.close('all')
                fig = plt.figure()
                ax = fig.add_subplot(111)

                # Create a basemap instance of the city with district
                city_map = mu._basemap_city()

                # Iterate through each district and paint it with the proper color.
                for key in crimes_by_sq.keys():
                    patches = []
                    for info, shape in zip(city_map.district_m_info, city_map.district_m):
                        if info['DIST_NUM'] == str(key):
                            patches.append(Polygon(np.array(shape), True))
                    pc = PatchCollection(patches, alpha=1, edgecolor='k', linewidths=1, zorder=2)

                    if int(crimes_by_sq[key]) == 0: # Meaning very little to no crimes in that district, we paint it in green
                        pc.set_facecolor('#00008B')
                    else:  # Otherwise we paint it in the proper color of the colormap
                        pc.set_facecolor(cmap(int(crimes_by_sq[key])))
                    ax.add_collection(pc)



                # Plot points representing each address with the proper street address annotation.
                for address in address_list:
                    address_lat, address_lon, street_address = address.lat, address.lon, address.street_address
                    x_address, y_address = city_map(address_lon, address_lat)
                    city_map.plot(x_address, y_address, marker='D',color='k')
                    plt.annotate(street_address, xy=(x_address, y_address), xycoords='data', xytext=(city_map(address_lon + 0.0015, address_lat + 0.0015)), textcoords='data', color='k', size='small', rotation=-35)


                # Add a color bar by using the _custom_colorbar function
                if int(max(crimes_by_sq.values())) > 1:
                    cbar = mu._custom_colorbar(cmap, len(labels), labels, shrink=1)
                    cbar.ax.tick_params(labelsize=16)
                    cbar.set_label('Number of crimes by Square mile in each District', size=16)
                    fig.canvas.set_window_title('Number of crimes by Square mile')
                else:
                    fig.canvas.set_window_title('No significant crimes for the selection. Please choose more crimes or years')
                    print ('No significant crimes for the selection. Please choose more crimes or years')

                # Set figuresize, save and show.
                plt.gcf().set_size_inches(15, 15)
                plt.show(block=show_city_block)





