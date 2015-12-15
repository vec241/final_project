__author__ = 'fnd212'
__reviewer__ = 'sb5518'

from addressClass import Address
import statistics
from statistics import CrimesDataFrame
import os
import Mapper
import pandas as pd


def address_analysis_output(address, crimes_database):
    """
    Receives a statistics.CrimesDataFrame object and an addressClass.Address object and an instance of an instance of
    the Address class. Prints statistics, map of crimes in the district where address is located
    and a time series of the crimes in the district and in a circumference of 1 mile radius from the address.
    
    :param: crimes_database
    :param address
    """
    if not isinstance(crimes_database, CrimesDataFrame): 
        raise TypeError('crimes_database must be a statistics.CrimesDataFrame object. {} received'.format(type(crimes_database)))
    if not isinstance(address, Address): 
        raise TypeError('address must be an addressClass.Address object.')

    os.system('clear')
    print('Crime Statistics for : ' + address.formatted_address + ':\n')

    if address.summary.dist_crime_density > address.summary.circ_crime_density:
        print ('Crime density within a 1 mile ratio around the address is {0:.2f} which is {1:.2f}% lower than the average of the District'.format(address.summary.circ_crime_density, 100 * (1 - address.summary.circ_crime_density/address.summary.dist_crime_density)))
    if address.summary.dist_crime_density < address.summary.circ_crime_density:
        print ('Crime density within a 1 mile ratio around the address is {0:.2f} which is {1:.2f}% higher than the average of the District'.format(address.summary.circ_crime_density, 100 * (address.summary.circ_crime_density/address.summary.dist_crime_density - 1)))
    if address.summary.dist_crime_density == address.summary.circ_crime_density:
        print ('Crime density within a 1 mile ratio around the address is {0:.2f} which is '
              'not significantly different than the average of the District'.format(address.summary.circ_crime_density))
    print ('Police Effectiveness (#arrests/#crimes): {0:.2f} %'.format(address.summary.dist_police_effectiveness*100))
    print ('Distance to the corresponding police station: {0:.2f} miles'.format(address.distance_to_police_station))
    print ('\n')
    print('Loading map...')

    Mapper.maps_builder.district_mapper(zip(crimes_database.Latitude, crimes_database.Longitude), address)

    try:
        address.summary.plot_indicator_density()
    except (statistics.EmptyList, statistics.EmptyCrimesDataFrame):
        #No Data to plot
        pass


def comparative_analysis_output(crimes_database, addresses): 
    """
    Receoves a list of instances of de Address class, and a crimes database.
    Prints a sorted pd.Series of the addresses by the security value (density of crimes in a circunference of 1 mile radius)
    Plots a map with the density of crimes in each district and the addresses in addresses array. 
    Plots a comparative time series of the density of crimes in the 1 mile radius circunference for the addresses in address array. 
    :param crimes_database
    :param: addresses
    """
    if not isinstance(crimes_database, CrimesDataFrame): 
        raise TypeError('crimes_database must be a statistics.CrimesDataFrame object')
    if (not isinstance(addresses, tuple)) and (not isinstance(addresses,list)): 
        raise TypeError('Addresses must be a list of addressClass.Adress objects')
    if not addresses: 
        raise ValueError('Empty array received')
    for address in addresses:
        if not isinstance(address,Address):
            raise TypeError('Addresses must be a list of addressClass.Adress objects')

    if len(addresses) == 1:
        print("For better comparative metrics, remember to save more than one address next time")
    
    addresses_crime_density = pd.Series({address.street_address:address.summary.circ_crime_density for address in addresses})
    addresses_crime_density.sort_values(ascending=True, inplace=True )

    print('Addresses ranking by crime density within a one mile ratio:\n')
    i = 1
    for address in addresses_crime_density.index:
        print ('[{}] {} \t Density: {:.2f}'.format(i, address, addresses_crime_density[address]))
        i = i+1
    
    print('Loading map...')
    Mapper.maps_builder.city_mapper(crimes_database, addresses)

    districts = [address.district for address in addresses]

    try:
        crimes_database.plot_indicator_per_district(districts,indicator='density')
    except (statistics.EmptyList, statistics.EmptyCrimesDataFrame):
        #No Data to plot
        pass
