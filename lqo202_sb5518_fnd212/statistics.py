__author__ = 'lqo202'

import pandas as pd
import databases_utils as du
from matplotlib import pyplot as plt
import indicators_utils as iu
import numpy as np
from numpy import sin, cos, pi
import geometry_utils as gu
import Projections as proj
from addressClass import Address


"""
This module contains the Statitics classes, regarding Chicago and by district.
In general both Classes summary data by month/year and then analyzes it.
Both computes 3 indicators: Density, Effectiveness and Effectiveness by mile square, which are the outputs. These are 
presented as summaries(to be called as attributes or functions accordingly to the class) for the district and the circle, 
also it gives a descriptive basic analysis of their evolution through time (mean, standard deviation, percentiles) 
and plots them.

* Class CrimesDataFrame: 
    This is a sub-class  from pandas data frame.
    Any subset of this, fill be a CrimesDataFrame object too by setting the constructor property.
    It computes the summaries in functions, using private and public ones. A brief description of the public ones 
    is following.
    Crime_density_by_district, effectiveness_police_by_district, effectiveness_sq_mile_by_district, are the methods
    that compute the indicators for all the districts.
    For parsymony, the plot just shows selected districts in the method plot_indicator_per_district, and also computes
    the summary descriptive statistics with the function get_summary_indicator_per_district.
    More details in each methods.

*  Class AddressStatistics
    First this class georeferences the address to give to results: a circle of 1 miles around it and the region of the 
    district where the point belongs to. Uses the addressclass as a utils.
    In contrast to Class CrimesDataFrame it creates attributes with values of the indicators (total and through time)
    The public methods in this class are for plotting the density(plot_indicator_density) and for getting the 
    basic statistics(get_summary_indicator)

More details can be found on each class and method.    
Some of the coded shown below was modified from its original version found on Stackoverflow    
"""

class MalformedCrimesDataFrame(Exception):
    pass

class EmptyList(Exception):
    pass

class EmptyCrimesDataFrame(Exception):
    pass

class CrimesDataFrame(pd.DataFrame):

    def __init__(self, *args, **kw):
        super(CrimesDataFrame, self).__init__(*args, **kw)

        for key in ['Year', 'Month', 'Arrest', 'District']:
            if key not in self.columns:
                raise ValueError('Database does not contain mandatory "{}" column.'.format(key))
        self.districts_contained = self.District.unique()

    @property
    def _constructor(self):
        """ A property set so that each modification or partition of the CrimesDataFrame isinstance
        keeps belonging to that class
        """
        return CrimesDataFrame

    def crime_density_by_district(self):
        """
        Computes the indicator of number of crimes per square mile by district in the whole Chicago area
        Its output is a dictionary with each value, where key is the number of district
        """
        crime_per_milesq = {}

        for district in self.districts_contained:
            data_district = self[self['District'] == district]
            try:
                crimes_per_district = iu.get_density(polygon=du.get_polygon(district), ammount=len(data_district))
            except iu.ZeroAreaPolygon as errmessage:
                crime_per_milesq[district] = np.nan
            else:
                crime_per_milesq[district] = crimes_per_district

        return crime_per_milesq

    def effectiveness_police_by_district(self):
        """
        This method does the calculation of the effectiveness of the police in each district.
        Returns a dictionary with the values, key is the number of district
        """
        effectiveness_police = {}
        for district in self.districts_contained:
            data_district = self[self['District'] == district]
            try:
                effectiveness_district = iu.effectiveness_police(data_district)
            except ValueError as errmessage:
                raise MalformedCrimesDataFrame(errmessage)
            else:
                effectiveness_police[district] = effectiveness_district

        return effectiveness_police


    def effectiveness_sq_mile_by_district(self):
        """
        This method returns the effectiveness of the police station by mile square in every district.
        It returns a  dictionary with the values, with key the number of district
        :return effectiveness_sq_mile
        """
        effectiveness_sq_mile = {}
        for district in self.districts_contained:
            data_district = self[self['District'] == district]
            try:
                effectiveness_sqmile_district = iu.effectiveness_sq_mile(polygon = du.get_polygon(district), data = data_district)
            except ValueError as errmessage:
                raise MalformedCrimesDataFrame(errmessage)
            except iu.ZeroAreaPolygon:
                effectiveness_sq_mile[district] = np.nan
            else:
                effectiveness_sq_mile[district] = effectiveness_sqmile_district

        return effectiveness_sq_mile

    def _validate_districts_array(self, Districts):
        """
        Receives a list of districts.
        This function confirms the districts to be valid, returning (raising) an exception or passing the code.
        If it is not a list or a tuple, a TypeError is raised.
        Also, validates that the list has valid districts (contained in the DB), if not raises a ValueError.        
        :param Districts
        """

        if not (isinstance(Districts,list) or isinstance(Districts,tuple)):
            raise TypeError('Districts should be a list or tuple containing district numbers')
        if not Districts:
            raise EmptyList('Empty list received')

        #If the database is empty    
        if not len(self): 
            raise EmptyCrimesDataFrame('Dataframe is empty')
        for district in Districts:
            if not district in self.districts_contained:
                raise ValueError('District {} not contained in the DB'.format(district))


    def plot_indicator_per_district(self, Districts, indicator='density'):
        """
        Shows a plot of the evolution per Year and month of the selected indicator in the desired districts.
        :param Districts: a list of districts to evaluate
        :param indicator: default is density, but it can compute effectiveness or effectiveness per mile sq
        :return: a figure with a line plot of the evolution in the inputted districts
        """
        try:
            self._validate_districts_array(Districts)
        except ValueError:
            raise EmptyCrimesDataFrame

        fig = plt.figure(figsize=(15,10))
        
        # Iterating by selected districts
        for district in Districts:

            data_dist = pd.Series(self._generate_db_month_district_indicator(district,indicator ))
            data_dist = data_dist.sort_index()
            plt.plot(data_dist.keys(), data_dist, '-s', label='District %i' %district)

        data_total = pd.Series(self._generate_db_month_district_indicator(0, indicator))
        data_total = data_total.sort_index()
        plt.plot(data_total.keys(), data_total, '-s', label='Chicago Average')
        
        
        # Labeling according to the desired indicator
        if indicator == 'density':
            plt.title("Evolution of Density of Crimes for selected districts")
            plt.ylabel('Density of Crimes by sq mile')

        elif indicator == 'effect':
            plt.title("Evolution of Effectiveness of Police for selected districts")
            plt.ylabel('Indicator percentage arrests')

        elif indicator == 'effectsq':
            plt.title("Evolution of Effectiveness per mile sq for selected districts")
            plt.ylabel('Effectiveness per mile sq')

        else:
            raise ValueError("Indicator not defined, try again.")

        plt.legend(loc="upper right")
        plt.xlabel('Year/Month')
        plt.grid()
        plt.show()
        

    def get_summary_indicator_per_district(self, Districts, indicator):
        """ Receives a list of districts to evaluate and an indicator (default is density, but can be
        effectiveness or effectiveness per mile sq)
        Computes some descriptive of the indicator (total by district) such as mean, variance percentiles by year in the
         inputted  Districts
        :param Districts
        :param indicator
        :return stats_total
        """
        try: 
            self._validate_districts_array(Districts)
        except ValueError: 
            raise EmptyCrimesDataFrame()

        stats_total = []

        for district in Districts:
            stats_total.append(self._generate_summary_district_indicator(district, indicator))

        stats_total = pd.concat(stats_total,axis=1)

        return stats_total


    def _generate_db_month_district_indicator(self, district, indicator):
        """ Receives a district and an indicator (default is 'density', but it can compute effectiveness('effectiveness')
        or effectiveness per mile sq ('effect_by_sqm')).Private function that selects the corresponding indicator from the desired district.
        It returns a series with the values per month/year. It raises an error if it is not one of the 3 defined indicators
        :param district
        :param indicator
        :return pd.Series
        """        
        if indicator == 'density':
            return pd.Series(self._generate_db_month_district(district)['density'], dtype=float)

        if indicator =='effect':
            return pd.Series(self._generate_db_month_district(district)['effectiveness'], dtype=float)

        if indicator == 'effectsq':
            return pd.Series(self._generate_db_month_district(district)['effect_by_sqm'], dtype=float)

        else:
            raise ValueError("Indicator not defined, try again!!!")

    def _generate_db_month_district(self, district=0):
        """
        Filters the DB according to the district and generates a dictionary with the number of
        crimes by month and year, for each indicator. 
        If district is set to zero, computes the total of all Chicago.
        As a note, it uses the following pd.datetime.strptime(str(int(month)).zfill(2)+str(year), '%m%Y')
        in order to create the index as a date type, making it easier to plot later.
         If there is no crime data, it sets the value Nan from numpy. Returns a a dictionary of the number of crimes
        :return data_ind
        """
        Years = self.Year.unique()
        data_ind = pd.DataFrame(columns=('density', 'effectiveness', 'effect_by_sqm'))

        #CHicago considers the total information by month/year
        if district == 0:
            area = 0
            for district in self.districts_contained:
                area += proj.PolygonProjection(du.get_polygon(district)).calculate_area_in_miles()

            for year in Years:
                data_district_year = self[self['Year'] == year]
                for month in range(1,13):
                    data_district_month = data_district_year[data_district_year['Month'] == month]
                    if len(data_district_month) == 0:
                        data_ind.loc[ pd.datetime.strptime(str(int(month)).zfill(2)+str(year), '%m%Y')] =[np.nan, np.nan, np.nan]
                    else:
                        data_ind.loc[ pd.datetime.strptime(str(int(month)).zfill(2)+str(year), '%m%Y')] = [ len(data_district_month)/ area,
                                                                                                            len(data_district_month[data_district_month['Arrest'] == True])*1.0 / len(data_district_month),
                                                                                                           (len(data_district_month[data_district_month['Arrest'] == True])*1.0 / len(data_district_month['Arrest']))/area]
        #Other case, it computes the indicator of the inputted district
        else:
            for year in Years:
                data_district_year = self[(self['District'] == district) & (self['Year'] == year)]
                for month in range(1,13):
                    data_district_month = data_district_year[data_district_year['Month'] == month]
                    if len(data_district_month) == 0:
                        data_ind.loc[ pd.datetime.strptime(str(int(month)).zfill(2)+str(year), '%m%Y')] =[np.nan, np.nan, np.nan]
                    else:
                        data_ind.loc[ pd.datetime.strptime(str(int(month)).zfill(2)+str(year), '%m%Y')] = [iu.get_density(polygon = du.get_polygon(district), ammount = len(data_district_month)),
                                                                                                            iu.effectiveness_police(data_district_month),
                                                                                                            iu.effectiveness_sq_mile(polygon = du.get_polygon(district), data =data_district_month)]
        return data_ind




class AddressStatistics(object):
    def __init__(self, address, db):
    
        for key in ['Year', 'Month', 'Arrest', 'Latitude', 'Longitude']:
            if key not in db.columns:
                raise ValueError('Database does not contain mandatory "{}" column.'.format(key))

        if not isinstance(address, Address):
            raise TypeError('Receive address is not of type addressClass.Address')

        self.address = address

        district = address.district
        district_db = self._filter_db_by_district(district,db)
        
        self.district = district
        
        #Setting attributes to total district info
        self.dist_crime_density = iu.get_density(polygon = du.get_polygon(district), ammount = len(district_db))
        self.dist_police_effectiveness = iu.effectiveness_police(data = district_db)
        self.dist_police_effectiveness_density = iu.effectiveness_sq_mile(polygon = du.get_polygon(district), data = district_db)

        #Setting attributes by month/year  from the district
        self.dist_crime_density_month = self._generate_db_month_district_indicator(district_db, 'density')
        self.dist_police_effectiveness_month = self._generate_db_month_district_indicator(district_db,'effect')
        self.dist_police_effectiveness_density_month = self._generate_db_month_district_indicator(district_db, 'effectsq')

        circle_data = self._get_data_crime_circle(db)

        #Setting attributes to circle, total info
        self.circ_crime_density = iu.get_density(polygon = self._get_circle_boundaries(), ammount = len(circle_data))
        self.circ_police_effectiveness = iu.effectiveness_police(data = circle_data)
        self.circ_police_effectiveness_density = iu.effectiveness_sq_mile(polygon = self._get_circle_boundaries(), data = circle_data)

        #Setting attributes to circle, by month/year
        self.circ_crime_density_month = self._generate_db_month_district_indicator(circle_data, 'density')
        self.circ_police_effectiveness_month = self._generate_db_month_district_indicator(circle_data,'effect')
        self.circ_police_effectiveness_density_month = self._generate_db_month_district_indicator(circle_data, 'effectsq')



    def plot_indicator_density(self):
        """
        Computes a summary per year of the number of crimes, by showing a plot of the evolution
        per Year and month of the same indicator
        :return a figure with a line plot of the evolution in the inputted districts
        """
        fig = plt.figure(figsize=(15, 10))
        plt.title("Evolution of Criminality")
        plt.ylabel('Density of Crimes by sq mile')     

        data_dist = self.dist_crime_density_month
        data_dist = data_dist.sort_index()
        plt.plot(data_dist.keys(), data_dist, '-s', label='District %i avg' % self.district)

        data_circle = self.circ_crime_density_month
        data_circle = data_circle.sort_index()
        plt.plot(data_circle.keys(), data_circle, '-s', label='1 mile ratio avg')

        plt.legend(loc="upper right")
        plt.xlabel('Year/Month')
        plt.grid()
        plt.show()


    def _generate_db_month_district_indicator(self, db, indicator):
        """ Receives a dataframe and an indicator
        Select the data of the desired indicator, converting them into a numeric (float) series.
        :param db
        :param indicator
        """
        if indicator == 'density':
            return pd.Series(self._generate_db_summarized_for_district(db)['density'], dtype=float)

        if indicator =='effect':
            return  pd.Series(self._generate_db_summarized_for_district(db)['effectiveness'], dtype=float)

        if indicator == 'effectsq':
            return  pd.Series(self._generate_db_summarized_for_district(db)['effect_by_sqm'], dtype=float)

        else:
            raise ValueError("Indicator not defined, try again!!!")

    def _generate_db_summarized_for_district(self, db):
        """
        This functions returns a dataframe of the indicators per month/year.
        It filters the data in year and then in month, so that it can compute the indicators in each subset (month and year).
        As a note, it uses the following pd.datetime.strptime(str(int(month)).zfill(2)+str(year), '%m%Y')
        in order to create the index as a date type, making it easier to plot later.                
        :param db: 
        """
        Years = db.Year.unique()
        data_ind = pd.DataFrame(columns=('density', 'effectiveness', 'effect_by_sqm'))
        for year in Years:
            data_year = db[db['Year'] == year]
            for month in range(1,13):
                data_district_month = data_year[data_year.Month == month]
                if len(data_district_month) == 0:
                    data_ind.loc[ pd.datetime.strptime(str(int(month)).zfill(2)+str(year), '%m%Y')] =[np.nan, np.nan, np.nan]
                else:
                    data_ind.loc[pd.datetime.strptime(str(int(month)).zfill(2)+str(year), '%m%Y')] = [iu.get_density(polygon=du.get_polygon(district_number=self.district), ammount= len(data_district_month)),
                                                                                                    iu.effectiveness_police(data=data_district_month),
                                                                                                    iu.effectiveness_sq_mile(polygon = du.get_polygon(self.district), data =data_district_month)]
        return data_ind

    def _filter_db_by_district(self,district,db):        
        return db[db['District']==district]


    def _get_circle_boundaries(self,radius=1):
        """
        Returns a list of coordinates (lat, long) with 100 points around the reference indicated, the default distance is 1 mile.
        Logic is that we have to split 360 degrees into the number of points desired (100), and then calculate the new
        coordinates for each one
        Original source was found in Stackoverflow question # 15886846, the actual version is a modified one
        :param radius
        :return circlePoints
        """
        #Radio of  earth in miles
        R = 3963

        #Number of points to be generated
        n = 50
        circlePoints = []

        center = (self.address.lat, self.address.lon)

        #Loop for getting each point and saving the lat lon
        for k in range(n):
            #Splitting the angle in the number of points and getting the cos and sin
            angle = pi*2*(k+1)/n
            anglevarx = radius*cos(angle)
            anglevary = radius*sin(angle)

            #Calculating the lattitude and longitude in function of the reference
            point = (center[0] + (180/ pi)*(anglevary/R),
                   center[1] + (180/pi)*(anglevarx/R)/cos(center[0]*pi/180))

            # add to list
            circlePoints.append(point)

        return circlePoints


    def _get_data_crime_circle(self,fullDataCrime):
        """ Receives a non-filtered DF
        Computes the database of the points inside the circle by filtering them by distance 
        :param fullDataCrime
        """        
        #Getting boundaries
        boundaries = self._get_circle_boundaries()

        districts = fullDataCrime['District'].unique()        
        
        if len(districts)== 0:
            raise ValueError("There are no districts in data")        

        district_polygons = {dist: du.get_polygon(dist) for dist in districts}

        districts_to_search = []
        
        #Filtering districts where the circle has values, to optimize time
        for bound in boundaries:
            for dist in district_polygons.keys():
                if dist not in districts_to_search: 
                    if gu.return_points_in_polygon([bound],district_polygons[dist]):
                        districts_to_search.append(dist)

        dataframe = fullDataCrime[fullDataCrime['District'].isin(districts_to_search)]

        #Getting the points inside of circle by distance (less equal than 1 mile)
        index_of_entries_in_circle = []

        for entry in dataframe.index:
            lat, lon = dataframe.ix[entry].Latitude, dataframe.ix[entry].Longitude

            if gu.calculate_distance_between_points(self.address.lat, self.address.lon, lat, lon) <= 1:
                index_of_entries_in_circle.append(entry)

        return dataframe.ix[index_of_entries_in_circle]


def address_analysis(crimes_database, address):
    """
    Receives  a statistics.CrimesDataFrame object and an addressClass.Address object.
    Creates an statistics.AddressStatistics object from a CrimesDataFrame and an Address object. 
    
    :param crimes_database, address
    :return: address_summary
    """
    if not isinstance(crimes_database, CrimesDataFrame): 
        raise TypeError('crimes_database must be a statistics.CrimesDataFrame object')
    if not isinstance(address, Address): 
        raise TypeError('address must be an addressClass.Address object.')

    if not address.summary:
        address_summary = AddressStatistics(address, crimes_database)

        return address_summary
