'''
Created on Dec 6, 2015

@author: rjw366

RecruitingData class houses the dataset and functions performed for finalProject.py
'''
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys

class recruitingData(object):
    
    def __init__(self,dataName):
        #Cleaning and storing data
        print("Loading dataset...")
        print("Looking in the same directory as finalProject.py for: candidate_info_v2.csv")
        try:
            df = pd.read_csv(dataName, index_col='candidate_id', parse_dates=['date_created'])
            #Dropping rows with: NaN in zip, Latitude, Longitude
            df = df.dropna(subset=['zip'])
            df = df.dropna(subset=['Latitude'])
            self.df = df.dropna(subset=['Longitude'])
            #Create year column
            self.df['Year_Created'] = self.df['date_created'].map(lambda x: x.year)
        except IOError:
            print("The data was not found")
            print("Make sure it's in the same directory as this file and try again")
            sys.exit(0)
        except:
            print("There was an error loading the data")
            print("Without data, I am useless. So I'll be ending now")
            sys.exit(0)
        print("Data successfully loaded")
        
    def getLatsAndLongsForYearCumulative(self,year):
        '''
        Gets a Series of longitudes and latitudes that are less than the provided year
        '''
        longs = self.df[self.df['Year_Created'].isin(range(2005,year+1))]['Longitude'].values
        lats = self.df[self.df['Year_Created'].isin(range(2005,year+1))]['Latitude'].values
        return lats, longs
    
    def getLatsAndLongsForYear(self,year):
        '''
        Gets a Series of longitudes and latitudes that are equal to the provided year
        '''
        longs = self.df[self.df['Year_Created'] == year]['Longitude'].values
        lats = self.df[self.df['Year_Created'] == year]['Latitude'].values
        return lats, longs
    
    def startSearch(self,typeOfSearch,year):
        '''
        Takes the year and the type of Search and directs it to the appropriate call
        '''
        if(typeOfSearch == "cumulative"):
            return self.getLatsAndLongsForYearCumulative(year)
        else:
            return self.getLatsAndLongsForYear(year)
    
    def printPlotBasemap(self,longs, lats, sizes=0):
        '''
        Taking in the latitudes and longitudes the program creates a map of the US
        and projects the coordinates on to the map, then printing it.
        '''
        # global ortho map centered on continental US
        lat_0=39.5; lon_0=-97.7
        # resolution = None to prevent long initial load 
        m1 = Basemap(projection='ortho',lon_0=lon_0,lat_0=lat_0,resolution=None)
        
        #Shrink map to only include US
        width = m1.urcrnrx - m1.llcrnrx 
        height = m1.urcrnry - m1.llcrnry 
        coef = 0.35 
        width = width*coef 
        height = height*coef 
        
        #Create new map zoomed in on US
        m = Basemap(projection='ortho',lon_0=lon_0,lat_0=lat_0,resolution='l',
           llcrnrx=-0.5*width,llcrnry=-0.5*height,urcrnrx=0.5*width,urcrnry=0.5*height)
      
        #Project Lats,
        x,y = m(longs,lats)
         
        #Pretty up map
        m.drawmapboundary(fill_color='black', zorder=-1)
        m.drawcountries()
        m.fillcontinents(color='white',lake_color='blue',zorder=0)
        
        #Plot points
        m.scatter(x,y,marker="o",c='r', alpha=.8)
        plt.show() 
    
        