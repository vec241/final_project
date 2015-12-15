'''
Created on Dec 15, 2015

@author: rjw366

Made an attempt to apply some clustering to the map to see a little more impact of where recruiting
was done. I failed because the Scaling algorothm moved all of my data to 1,0,-1. My guess is 
because of the large spread of the data.
'''
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def coordBinningDBSCAN(coords):
    coords = StandardScaler(with_std=False).fit_transform(coords)
    # Compute DBSCAN
    print(coords)
    db = DBSCAN().fit(coords)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    clusters = pd.Series([coords[labels == i] for i in xrange(n_clusters_)])
    print(clusters)
    print('Estimated number of clusters: %d' % n_clusters_)
    lon = []
    lat = []
    for i, cluster in clusters.iteritems():
        if len(cluster) < 3:
            representative_point = (cluster[0][1], cluster[0][0])
        else:
            representative_point = getNearestPoint(cluster, getCentroid(cluster))
        lon.append(representative_point[0])
        lat.append(representative_point[1])
    rs = pd.DataFrame({'lon':lon, 'lat':lat})
    print(rs)
    
def getCentroid(points):
    n = points.shape[0]
    sum_lon = np.sum(points[:, 1])
    sum_lat = np.sum(points[:, 0])
    return (sum_lon/n, sum_lat/n)

def getNearestPoint(set_of_points, point_of_reference):
    closest_point = None
    closest_dist = None
    for point in set_of_points:
        point = (point[1], point[0])
        dist = np.linalg.norm(point_of_reference-point).meters
        if (closest_dist is None) or (dist < closest_dist):
            closest_point = point
            closest_dist = dist
    return closest_point

