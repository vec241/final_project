# DS-GA-1007_Final-Project

Authors
-------
- Sebastian Brarda (sb5518@nyu.edu)
- Felipe Ducau (fnd212@nyu.edu)
- Luisa Quispe Ortiz (lqo202@nyu.edu)


What is it?
-----------
V1.0

This program was designed as the Final Project for DS-GA 1007, Programming for Data Science course at NYU. It was
programmed by Felipe Ducau, Sebastian Brarda, and Luisa Quispe Ortiz during the Fall semester of 2015.

The goal of the program is to provide an interactive environment to visualize and analyze the crime evolution by address
and district in the city of Chicago during the last years. A potential (but not only )use case would be for someone who is looking to
move to Chicago (rent a house or apartment), and wants to check how safe the different addresses of the real state listings are.

Data used for analysis and visualization comes from the City of Chicago Open Data portal: https://data.cityofchicago.org/

The program will ask the user to select a time frame (in years) and one or more types of crime. This initial filtering
of the data will remain for the whole cycle (it is not possible to select further years or crimes after this initial selection
unless the program is restarted).

After that, the program will ask the user to introduce a valid address in Chicago, which will be validated through the
Google Maps API. Please take into consideration that if Google maps consider an address valid, this program will consider
it valid as well.

If the address introduced is correct, the program will display a Heat Map of the district where the address of interest is 
located in order to provide a useful visualization of the crime rate in the surroundings. Severalother useful statistics 
will be printed in console.

After this, user will have the option to save or erase the address, and can repeat the process by adding further addresses
and visualizing their respective heat maps and crime statistics.

Another option that the program provides, is to make a comparative map and analysis. In this case, comparative statistics
and charts will be displayed based on the addresses that the user decided to save/keep. A map of the entire city will be
displayed, assisting the comparison between the different addresses/districts and the crime density in each of them.

User will have the possibility to repeat analyses and add/erase addresses until he/she decides to finalize the program
by entering 'Quit' or CTRL+C.



Installation instructions
-------------------------

- This program is optimized to work in Linux/Unix

- If you do not have the required packages installed, please check INSTALL_INSTRUCTIONS.md files for instructions on how to install them.

- Please download the Main Database for this program located at: https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD
Please save the database in the /Databases folder located inside the main directory of the program.

- It is also required to have a GoogleMaps API key in the main directory of this program. If you do not have one, you can create it, please
follow the instruction at: https://developers.google.com/maps/documentation/geocoding/get-api-key 
After getting the key, you should save it in a file called 'gmapskey.key' in the program directory.

ATTENTION
---------

Please make sure that you have installed the following python packages before attempting to run the program. Otherwise,
the program will fail:

- pandas
- numpy
- matplotlib
- scipy
- fiona
- re
- shapely
- os
- googlemaps
- basemap

Directories, Files and Modules
------------------------------

	/DS-GA-1007_Final-Project
	- main.py
	- Area.py
	- CircleDensity.py
	- addressClass.py
	- Mapper.py
	- Mapper_utils.py
	- databases_utils.py
	- defined_exceptions.py
	- geometry_utils.py
	- indicators_utils.py
	- interface_utils.py
	- Projections.py
	- statistics.py
	- INSTALL_INSTRUDCTIONS.MD
	- README.MD
	- results.py
	
	/DS-GA-1007_Final-Project/Databases
	- Crimes_-_2001_to_present.csv    ------> This is the only file that should be downloaded apart. The rest of the files/modules should come by default.
	- Police_Stations.csv

	/DS-GA-1007_Final-Project/Databases/districts
	- geo_fthy-xz3r-1.cst
	- geo_fthy-xz3r-1.dbf
	- geo_fthy-xz3r-1.prj
	- geo_fthy-xz3r-1.shp
	- geo_fthy-xz3r-1.shx

	/DS-GA-1007_Final-Project/tests
	- csv_for_test.csv
	- test_area.py
	- test_mapper.py
	- test_results.py
	- test_db_utils.py
	- test_address.py
	- test_statistics.py
	- test_geometry_utils.py
	- test_indicators_utils.pu

Testing
-------

- All the tests ar in the test folder.
- To run all the tests together you can do it with the following bash command: python -m unittest discover ./test 
- Otherwise, to run them individually, you should move the desired test from the ./test folder to the main folder of the program.
- Please take into account that some tests require the csv_for_test.csv to run.


Copyright and licencing information:
------------------------------------

Some parts of the Mapper module were inspired by the following two examples:
	# The Heat Map of the district is inspired in the following example: http://bagrow.com/dsv/heatmap_basemap.html
	# The _custom_colorbar used for the city_mapper was inspired in the code provided in: http://beneathdata.com/how-to/visualizing-my-location-history/

# The _get_boundaries method in the StatisticsRanking module was inspired in question #15886846 of Stackoverflow 

Thank you very much for such inspiring examples!

References and links
--------------------

Main Database
https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD

Police Stations: 
https://data.cityofchicago.org/api/views/z8bn-74gv/rows.csv?accessType=DOWNLOAD 

Other considerations
--------------------

The metrics offered for the addresses in districts 14 and 12 might not be perfect. The reason is that there actually exists a
district 13 that is not plotted because it does not has a police station so it does not make sense from a criminallistic point of view.
As a consequence, in reality both Police Stations of districts 14 and 12 divide the crimes between them, which is clear by reading the entries of
the database. The direct consequence for our program is that density metrics for District 14th might be slightly overestimated, while density
metrics of district 12 might be slighly underestimated. The rest of the districs have accurate metrics.




We hope that you really enjoy the program and find it useful. Please do not hesitate to contact us in case you find any bug or had a feature request!!


