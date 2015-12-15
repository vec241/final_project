INSTALL INSTRUCTIONS
--------------------

This is an informal guide to install the required packages/dependencies in order to run the program
and by no mean is the only way to do it.


The easiest way to install the required packages is through PIP or Anaconda. 

You can install PIP by introducing the following line in your terminal:

sudo apt-get install python-pip

Afterwards you can proceed to install each required package:

Googlemaps
sudo pip install googlemaps

Fiona
sudo apt-get install libgdal-dev
sudo pip install fiona

Shapely
sudo pip install shapely

Matplotlib
sudo apt-get install python-matplotlib

Numpy
sudo pip install numpy

Pandas
sudo pip install pandas

Basemap
sudo apt-get install python-mpltoolkits.basemap
sudo pip install gdal


Alternatively, in Anaconda:

conda install shapely
conda install gdal
conda install basemap
conda install fiona
conda install googlemaps

