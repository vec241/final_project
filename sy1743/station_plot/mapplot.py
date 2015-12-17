import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#author: Muhe Xie
#netID: mx419
#date: 12/05/2015

"""
This module contains a class to plot frequency results on the basemap, there methods are provided to draw frequecny map,
draw  frequecny map of top k stations, draw heatmap
"""

class MapPlot(object):
    """
    This class contains methods to visualize the station location data and frequency data on the map
    """

    def __init__(self,dots,month,year):
        self.dots = dots
        longs = dots['long']
        longs = longs.tolist()
        self.longs = [float(x) for x in longs]
        lats = dots['lat']
        lats = lats.tolist()
        self.lats = [float(x) for x in lats]
        self.freqs = dots['freq']
        self.v_max = self.freqs.max()
        self.v_min = self.freqs.min()
        self.v_median = self.freqs.median()
        self.freqs_list = self.freqs.tolist()
        self.month = str(month)
        self.year = str(year)

        

    def get_red_color(self,maxvalue,minimunvalue,this_value):
        #get the red distribution in the rgb color
        ranger = maxvalue - minimunvalue
        return 1.0 - float((this_value-minimunvalue))/float(ranger)

    def get_blue_color(self,maxvalue,minimunvalue,this_value):
        #get the blue distribution in the rgb color
        ranger = maxvalue - minimunvalue
        return 1.0 - float((this_value-minimunvalue))/float(ranger)

    def get_color_tuple(self,freq):
        #get the rgb color tuple
        if freq>=self.v_median:
            a = self.get_red_color(self.v_max,self.v_median,freq)
            return (1,a,a)
        else:
            a = self.get_blue_color(self.v_median,self.v_min,freq)
            return (a,a,1)

    def draw_freq_map(self):
        """
        Plot citibike station into map.
        """
        plt.figure(figsize=(20,10))
        plt.title('Frequency Distribution of Citi Bike Stations in ' +self.year+'.'+self.month) 
        #range of map
        map = Basemap(projection='merc', resolution = 'i',  area_thresh = 0.1,llcrnrlon=-74.04, llcrnrlat= 40.68,urcrnrlon= -73.937599, urcrnrlat=40.7705)
        map.drawcoastlines(color = 'r')
        map.drawcountries(color = 'aqua')
        map.drawmapboundary(zorder=0)

        x2,y2 = map(self.longs,self.lats)
        for i in range(len(x2)):
            map.plot(x2[i], y2[i], marker = 'o',color = self.get_color_tuple(self.freqs_list[i]),markersize=16,zorder = 1)
        # 2 points as legend
        legend_high_x,legend_high_y = map(-74.036,40.7685)
        legend_low_x,legend_low_y = map(-74.036,40.763)
        map.plot(legend_high_x,legend_high_y,marker = 'o',color = (1,0,0),markersize=20,zorder = 1)
        map.plot(legend_low_x,legend_low_y,marker = 'o',color = (0,0,1),markersize=20,zorder = 1)
        plt.text(legend_high_x+300, legend_high_y-100, 'High Freq',fontsize=12)
        plt.text(legend_low_x+300, legend_low_y-100, 'Low Freq',fontsize=12)
        plt.show()

    def draw_top_k_freq_map(self,k):
        """
        Plot station with top k highest frequency station.
        """

        top_k_index = self.dots.sort('freq',ascending=False)[:k].index
        plt.figure(figsize=(20,10))
        plt.title('Top '+str(k)+' frequency citi bike stations in '+ self.year+'.'+self.month) 
        map = Basemap(projection='merc', resolution = 'i',  area_thresh = 0.1,llcrnrlon=-74.04, llcrnrlat= 40.68,urcrnrlon= -73.937599, urcrnrlat=40.7705)
        map.drawcoastlines(color = 'r')
        map.drawcountries(color = 'aqua')
        map.drawmapboundary(zorder=0)

        x2,y2 = map(self.longs,self.lats)
        for i in top_k_index:
            map.plot(x2[i], y2[i], marker = 'o',color = self.get_color_tuple(self.freqs_list[i]),markersize=14,zorder = 1)
 
            plt.text(x2[i]+200, y2[i], self.dots.ix[i]['name'],fontsize = 7)
        # 2 points as legend
        legend_high_x,legend_high_y = map(-74.036,40.7685)
        legend_low_x,legend_low_y = map(-74.036,40.763)
        map.plot(legend_high_x,legend_high_y,marker = 'o',color = (1,0,0),markersize=20,zorder = 1)
        map.plot(legend_low_x,legend_low_y,marker = 'o',color = (0,0,1),markersize=20,zorder = 1)
        plt.text(legend_high_x+300, legend_high_y-100, 'High Freq',fontsize=12)
        plt.text(legend_low_x+300, legend_low_y-100, 'Low Freq',fontsize=12)
        plt.show()
        
    def draw_heat_map(self):
        """
        Plot heatmap by station frequency
        """

        plt.figure(figsize=(20,10))
        plt.title('Heat Map of Citi Bike Stations in '+self.year+'.'+self.month) 
        map = Basemap(projection='merc', resolution = 'i',  area_thresh = 0.1,llcrnrlon=-74.04, llcrnrlat= 40.68,urcrnrlon= -73.937599, urcrnrlat=40.7705)
        
        map.drawcoastlines(color = 'r')
        map.drawcountries(color = 'aqua')
        map.drawmapboundary(zorder=0)

        x2,y2 = map(self.longs,self.lats)
        for i in range(len(x2)):
            map.plot(x2[i], y2[i], marker = 'o',color = self.get_color_tuple(self.freqs_list[i]),markersize=7,zorder = 1)

        ny = 20 #number of vertical grids for heat map
        x_range =  max(self.longs) - min(self.longs)
        y_range =  max(self.lats) - min(self.lats)
        y_step = y_range/float(ny) #height of grid
        ratio = x_range/y_range
        nx = int(ny*ratio) #number of horizonal grids for heat map
        x_step = x_range/float(nx) #width of grid


        # compute appropriate bins to histogram the data into
        lon_bins = np.linspace(min(self.longs), max(self.longs), nx+1)
        lat_bins = np.linspace(min(self.lats), max(self.lats), ny+1)

        density_matrix = np.ones((ny,nx))
        #get the freqency density matrix 
        for i in range(ny):
            for j in range(nx):
                x_upper_left,y_upper_left = self.get_locaion_by_row_column_index(i,j,min(self.longs),max(self.lats),x_step,y_step)
                density_matrix[i][j] = self.get_freq_by_location(x_upper_left,x_upper_left+x_step,y_upper_left-y_step,y_upper_left,min(self.freqs_list),self.longs,self.lats,self.freqs_list,x_step,y_step)
                
        
        lon_bins_2d, lat_bins_2d = np.meshgrid(lon_bins, lat_bins)
        xs, ys = map(lon_bins_2d, lat_bins_2d) 

        plt.pcolormesh(xs, ys, np.flipud(density_matrix),alpha = 1)
        plt.colorbar(orientation='vertical')

        plt.show()



    def get_freq_by_location(self,long_start,long_end,lat_start,lat_end,lowest_freq,longs,lats,freqs,x_step,y_step):
        #this function will get the max frequecy in the given zone
        freq_sum = 0
        n_count = 0
        freq_max = lowest_freq
        for index_i in range(len(longs)):
            if longs[index_i]>= long_start and longs[index_i]<= long_end and lats[index_i]>= lat_start  and lats[index_i]<= lat_end:
                if freq_max < freqs[index_i]:
                    freq_max = freqs[index_i]
        return freq_max

    def get_locaion_by_row_column_index(self,row_index,column_index,long_start,lat_end,x_step,y_step):
        #this function will get the range of a grid by the row and column index
        x_upper_left = long_start+column_index*x_step
        y_upper_left =lat_end - row_index*y_step
        return x_upper_left,y_upper_left
    
    

