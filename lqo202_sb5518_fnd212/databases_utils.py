__author__ = 'fnd212'
__reviewer__ = 'sb5518'

"""
This module contains a set of functions meant to clean and filter Data of the program based on user input:

Methods:

- clean_crimes_db(db_path)
- def setup_crimes_db(path)
- get_crimes_db(path=CRIMES_DB_PATH)
- filter_db_by_timeframe(db, key)
- filter_db_by_crime(db, key='Primary Type')
- get_polygon(district_number, shp_file_location = SHP_FILE_PATH)
- get_police_station_coordinates(district_number, db_police = PS_DB_PATH)
- get_district_from_lat_lon(reference_point)

"""

import fiona
import pandas as pd
import re
from shapely.geometry import Point, Polygon
from interface_utils import yesno_question, get_timeframe_from_user, get_options_from_user
import numpy as np
import defined_exceptions
import os

# This is the list of Valid District numbers of Chicago.
DISTRICTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22, 24, 25]

# These are the paths of the cleaned and original Databases used for analysis
CRIMES_DB_PATH = './Databases/Crimes_-_2001_to_present_CLEAN.csv'
ORIGINAL_CRIMES_DB_PATH = './Databases/Crimes_-_2001_to_present.csv'

# Columns of the crimes database used in the program
USED_DB_COLUMNS = ['Date','Primary Type', 'Arrest', 'District', 'X Coordinate', 'Y Coordinate', 'Year',
                    'Latitude', 'Longitude', 'Month' ]

# Default path for the database containing the police stations information
PS_DB_PATH = './Databases/Police_Stations.csv'
# Default path for the database containing shapes of the districts in Chicago
SHP_FILE_PATH = './Databases/districts/geo_fthy-xz3r-1'



def clean_crimes_db(db_path):
    """
    Opens and removes the unused columns of the DB and cleans
    na values, all in place. Returns a Cleaned Database
    :param  db_path
    :return db

    """
    db = pd.read_csv(db_path)

    # Drop unused columns
    for column in db.columns:
        if column not in USED_DB_COLUMNS:
            db.drop(column,axis=1,inplace=True)
        db.dropna(inplace=True)

    # Remove entries for invalid (not within predefined) districts.
    for district in db.District.unique():
        if district not in DISTRICTS:
            db.drop(db[db.District == district].index, axis=0,inplace=True)

    # Get a column with the month of the crime
    db['Month'] = db.Date.map(lambda x: x.split('/')[1])

    return db


def setup_crimes_db(path=CRIMES_DB_PATH):
    """
    Checks if the database is present and clean.
    If not clean, pre-processes the database and returns it.
    If the database is present and clean, returns None.
    :param  path
    :return db_crimes_clean

    """

    db_name = CRIMES_DB_PATH.split('/')[-1]
    orig_db_name = ORIGINAL_CRIMES_DB_PATH.split('/')[-1]

    # Check if the Database is clean, and start the cleaning process if required.
    if not db_name in os.listdir('./Databases/'):
        if orig_db_name in os.listdir('./Databases/'):

            print('Crimes database needs to be pre-processed before start running the program. This process might take several minutes. Please wait.')
            db_crimes_clean = clean_crimes_db(ORIGINAL_CRIMES_DB_PATH)
            print('Pre-processing completed.')

            # Offer the user the possibility to save the pre-processed DB
            if yesno_question('Do you want to save the pre-processed to {} DB for the next time?'.format(CRIMES_DB_PATH)):
                print('Please wait while saving...')
                db_crimes_clean.to_csv(CRIMES_DB_PATH)
                
            return db_crimes_clean

        # If the Database is not in the Databases folder inside the program directory, raise exception
        else:
            raise defined_exceptions.FatalError('Crimes database not found in {} \nYou can download the database from https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD and try again \nDatabase should be saved in the "Databases" folder inside the program Directory '.format(ORIGINAL_CRIMES_DB_PATH))

    return None



def get_crimes_db(path=CRIMES_DB_PATH):
    """
    Loads the crimes database from path (default is CRIMES_DB_PATH)
    Asks the user what to do if database is not found.
    :param path
    :return db

    """
    db = setup_crimes_db(CRIMES_DB_PATH)
    if not db is None:
        return db

    #Specify variable types for faster loading of the DB
    db_types = {'District':np.int16, 'X Coordinate':np.int32, 'Y Coordinate':np.int32,
    'Year':np.int16, 'Latitude':np.float64, 'Longitude':np.float64, 'Date':str,
    'Primary Type':str, 'Arrest':bool, 'Month':np.int16}

    db_true_values = ['True']
    db_false_values = ['False']

    print('\nLoading crimes database...')
    db = pd.read_csv(path, dtype=db_types, true_values = db_true_values,
                    false_values=db_false_values,index_col=0)

    return db


def filter_db_by_timeframe(db, key='Year'):
    """
    Receives a Pandas DataFrame, asks user for a time-frame and
    filters the database accordingly.
    key optional argument specifies the column name of the years.

    :param db
    :return db
    """

    if not isinstance(db, pd.DataFrame):
        raise TypeError('Invalid object received. Expecting pandas.DataFrame')
    if key not in db.columns:
        raise ValueError('Database does not contain "{}" label to filter.'.format(key))

    # Ask user to select a TimeFrame based on the available Years in the DB
    min_year, max_year = get_timeframe_from_user(max(db.Year),min(db.Year))

    db = db[db.Year >= min_year]
    db = db[db.Year <= max_year]

    return db

def filter_db_by_crime(db, key='Primary Type'):
    """
    Receives a dataframe, asks user which crimes is interested in,
    filters and returns the database accordingly.
    key optional argument indicates which is the column where the crimes are listed.

    :param db
    :return db
    """

    if not isinstance(db, pd.DataFrame):
        raise TypeError('Invalid object received. Expecting pandas.DataFrame')

    if key not in db.columns:
        raise ValueError('Database does not contain "{}" label to filter.'.format(key))

    # Show available crime types, receive selections from user and filter accordingly.
    selected_crimes = get_options_from_user(db['Primary Type'].unique(), multiple=True)
    db = db[db['Primary Type'].isin(selected_crimes) == True]

    return db


def get_polygon(district_number, shp_file_location = SHP_FILE_PATH):
    """
    Reads the value in district_number and returns a list of tuples of coordinates
    that form the polygon for the requested district number.

    Uses the information contained in shp_file_location as source.

    ValueError is raised is the district number is not found in the SHP file

    :param district_number, shp_file_location
    :return: List of tuples containing coordinates in format (lat,lon)
    """

    try:
        district_number = int(district_number)
    except TypeError:
        raise TypeError('district_number must be an integer or a string representing an integer.')
    except ValueError:
        raise ValueError('Not a valid integer representation received.')

    shape = fiona.open(shp_file_location+'.shp')

    for item in shape.items():
        if int(item[1]['properties']['DIST_NUM']) == district_number:
            coordinates = item[1]['geometry']['coordinates']
            
            coordinates_lat_lon = [(coordinate[1], coordinate[0]) for coordinate in coordinates[0]]
            shape.close()
            return coordinates_lat_lon
            
    shape.close()
    raise ValueError('District number {} not contained in {}'.format(district_number,shp_file_location))


def get_police_station_coordinates(district_number, db_police = PS_DB_PATH):
    """
    Receives a district number and looks for the location of the police station
    in db_police.
    db_police optional argument specifies the location of the database.

    :param district_number, db_police
    :return police_station_coordinates
    """

    try:
        district_number = int(district_number)
    except TypeError:
        raise TypeError('district_number must be an integer or a string representing an integer.')
    except ValueError:
        raise ValueError('Not a valid integer representation received.')

    try:
        police_stations_db = pd.read_csv(db_police)
    except IOError:
        raise IOError('Police database {}  does not exist'.format(db_police))

    if str(district_number) not in police_stations_db.DISTRICT.values:
        raise ValueError('{} is not a valid district number'.format(district_number))


    ps_location = police_stations_db.LOCATION[police_stations_db.DISTRICT == str(district_number)]

    # Get the string value
    ps_location = ps_location.iloc[0]
    ps_coordinates = re.findall('\((.*)\)',ps_location)

    ps_coordinates = ps_coordinates[0].split(',')

    #Cast coordinates to float and list to tuple
    police_station_coordinates = tuple([float(coordinate) for coordinate in ps_coordinates])

    return police_station_coordinates



def get_district_from_lat_lon(reference_point):
    """
    Evaluates the reference point (lat,lon) given and outputs a value with the number of district it belongs to.
    Raises an exception if the reference point does not belong to any of the districts (in chicago)

    :param reference_point
    :return point_in_district
    """

    try:
        if len(reference_point) != 2:
            raise ValueError('Object of the form latitude,longitude \
                            for the reference point was expected.')

    except TypeError:
        raise TypeError('Tuple or list containing latitude and longitude was expected.')

    point_in_district = 0

    for district in  DISTRICTS:
        reference = Point(reference_point[0], reference_point[1])
        if Polygon(get_polygon(district)).contains(reference):
            point_in_district = district
            break

    if not point_in_district:
        raise ValueError('The coordinates introduced are not inside a district in Chicago')

    return point_in_district

