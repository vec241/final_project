'''
This program is on generating all the graphs used in the analysis according to user input.


'''
import matplotlib.pyplot as plt
import pandas as pd

def all_area_all_year_by_city(data):
    #show total complain number in one city for 6 years
    data=data['city']
    frequency=data.value_counts()[:10]
    frequency.plot(kind='bar',color='lightblue')
    plt.title('Total Complaint From 2010 To 2015 in NYC By City')
    plt.xlabel('city')
    plt.ylabel('number of complaints')
    plt.gcf().subplots_adjust(bottom=0.3)
    #print frequency
    plt.show()
    
def get_sorted_complaint_data_by_city(data,city):
    
    data=data[data['city']==city]
    summary=data.groupby(['complain_type','year']).size().unstack()
    df=pd.DataFrame(summary)
    df.columns=['2010','2011','2012','2013','2014','2015']
    #print df.columns[1:6]
    df['sum']=df[['2010','2011','2012','2013','2014','2015']].sum(axis=1)
    df.sort(columns=['sum'],ascending=False,inplace=True)
    return df
    
def specific_city_all_year_first_5_complain(data,city):
    #show the top 5 complaint types in borough according to user input in last 6 years
    plot_df=data.head(5)
    plot_df=plot_df[plot_df.columns[:-1]]
    print "First 5 Complains In ",city
    print plot_df
    colors=['yellowgreen','red','gold','lightskyblue','lightcoral','violet']
    plot_df.plot(kind='bar',color=colors)
    plt.xticks(rotation=30)
    plt.gcf().subplots_adjust(bottom=0.3)
    plt.show()
    
def specific_city_all_year_piechart(data,city):
    #show the percentage of top 10 complaint type in the borough according to the input 
    total=sum(data['sum'])
    data['pct']=data['sum']/total
    data['pct_for_legend']=data['pct'].map(lambda x: '{:.2%}'.format(x))
    plot_data=data.head(10)
    chosen_cols_to_show=['2010','2011','2012','2013','2014','2015','sum','pct_for_legend']
    print 'Top 10 Complaint Types in {}'.format(city)
    print plot_data[chosen_cols_to_show]
    labels=plot_data.index.tolist()
    plt.title('Top 10 Complaint Types')
    colors=['yellowgreen','red','gold','lightskyblue','lightcoral','blue','pink','yellow','grey','violet']
    labels_new=['{0} - {1}'.format(i,j) for i,j in zip(labels,plot_data.pct_for_legend)]
    (patches,texts)=plt.pie(plot_data.pct, colors=colors,shadow = True, startangle = 90)
    plt.legend(patches,labels_new,bbox_to_anchor=(1,0.9),fontsize=10)
    plt.show()
    
    
    
def plot_location_type_for_particular_complaint_in_city(location_type_data,city,complaint_type):
    #according to the user input complaint type, show the location where there were issues that led to complain.
    city_data=location_type_data[location_type_data['city']==city]
    complaint_type_data=city_data[city_data['complaint_type']==complaint_type]
    frequency=complaint_type_data['location_type'].value_counts()[:10] #location_type series
    frequency=pd.DataFrame(frequency)
    frequency.columns=['counts']
    frequency.index.name=['loaction_type']
    print 'Location Distribution of {0} in {1}'.format(complaint_type,city)
    print frequency
    length=len(frequency)  
    color=['yellowgreen','red','gold','lightskyblue','lightcoral','blue','pink','yellow','grey','violet']
    frequency.plot(kind='bar',color=color[:(length+1)])
    plt.title('First {0} Complaint Location of {1} '.format(length,complaint_type))
    plt.xticks(rotation=30)
    plt.subplots_adjust(bottom=0.25)
    plt.show()

def time_trend_line(data,city):
    #show the line chart on the number of complaints in different hours
    data=data[data['city']==city]
    frequency=data['hour'].value_counts()
    frequency=frequency.sort_index()
    xscale=range(0,24,2)
    plt.plot(frequency)
    plt.xlim(0,23)
    ax=plt.gca()
    ax.set_xticks(xscale)
    plt.xlabel('Hour')
    plt.ylabel('Number')
    plt.title('Time Trend Line in '+city)
    plt.show()
    
    
    

def getstatus(data,zipcode):
    data=data[data['incident_zip']==zipcode]
    #print data['facility_status'].unique()
    xstatus=data['facility_status']
    return xstatus

def get_data_for_piechart(data,zipcode):
    xstatus=getstatus(data,zipcode)
    frequency=xstatus.value_counts()
    #print frequency.index
    return frequency   
    
def status_piechart(frequency):
    #show the status of complaints (closes, assigned, etc)
    plt.figure(num = 1, figsize=(6, 6))
    ax=plt.gca()
    ax.set_aspect('equal')
    frequency=pd.DataFrame(frequency)
    frequency.columns=['counts']
    #print frequency
    labels=frequency.index.unique().tolist()
    counts=frequency.counts
    frequency['pct']= frequency['counts']/sum(counts)
    frequency['pct']=frequency['pct'].map(lambda x: '{:.2%}'.format(x))
    #print frequency
    #for (counts,pct) in zip(frequency.counts,frequency.pct):
        #print counts,pct
    length=len(labels)
    explode = [0.1]+[0]*(length-1)
    plt.title('The Status of Facility')
    colors=['yellowgreen','red','gold','lightskyblue','lightcoral']
    labels_new=['{0} - {1}'.format(i,j) for i,j in zip(labels,frequency.pct)]
    (patches,texts)=plt.pie(frequency.counts, colors=colors, explode=explode,shadow = True, startangle = 90)
    plt.legend(patches,labels_new,bbox_to_anchor=(0.3,0.9),fontsize=10)
    plt.show() 

