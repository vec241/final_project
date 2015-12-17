## Installation
basemap and GEOS (Geometry Engine - Open Source) library are required for showing features on the map, both two libraries are already downloaded in the compressed file: **basemap-1.0.7.tar.gz**.
The below instructions are referenced from:              http://matplotlib.org/basemap/users/installing.html
### step 1: Numpy, python and matplotlib
Install numpy 1.0.0 or later, python 2.4 or later, matplotlib 1.0.0 or later. **If they are installed, go to step2**.
### step 2: Untar the file
Untar the basemap-1.0.7.tar.gz file, and and cd to the **basemap-1.0.7** directory
### step 3: Install GEOS library
**1 If you don’t have GEOS library on your system**, you can build it from the source code included with basemap by using following commands in the ubuntu command line:
* cd to the geos-3.3.3 directory (it is under the directory basemap-1.0.7)
```sh
$ cd geos-3.3.3
```
* setting environment variable GEOS_DIR and Install the GEOS library
```sh
$ export GEOS_DIR=<the directory you want the libs and headers to go> 
##I recommend to install it in your home directory, for example:/home/ds-ga-1007
##Do not have space before and after the '=' symbol, a correct example is like this: export GEOS_DIR=/home/ds-ga-1007
##If any permission wrong happens, use sudo su to get the super user authority, or get root authority

$ ./configure --prefix=$GEOS_DIR
##I recommend you to get super user authority here
##The result of running this command is like: 
##Swig: false 
##Python bindings: false
##...

$ sudo su ##then enter the password to get super user authority
$ make; make install ## It may take a bit time, ignore the warnings if any
```

**2 If you already have GEOS library on your system**, just set the environment variable GEOS_DIR to point to the location of libgeos_c and geos_c.h (if libgeos_c is in /usr/local/lib and geos_c.h is in /usr/local/include, set GEOS_DIR to /usr/local). Then go to next step. 

### step 4: Install basemap
1 cd to the geos-3.3.3 again, export GEOS_DIR and do the configure again, it is very important!

2 cd back to the top level basemap directory (**basemap-1.0.7**) and run the usual **python setup.py install**. Check your installation by running **from mpl_toolkits.basemap import Basemap** at the python prompt.

 ```sh
$ cd geos-3.3.3
$ export GEOS_DIR=<the directory you want the libs and headers to go> 
##It is important to repeat this again! Otherwise the installation maigt fail
##I recommend to install it in your home directory, for example:/home/ds-ga-1007
##Do not have space before and after the '=' symbol, a correct example is like this: export GEOS_DIR=/home/ds-ga-1007


$ ./configure --prefix=$GEOS_DIR

$ cd basemap-1.0.7


$ python setup.py install

##Check whether you have installed successfully
$ python
$ from mpl_toolkits.basemap import Basemap 
##If this works, the installation is OK
```

