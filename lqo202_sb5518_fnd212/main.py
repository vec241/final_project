__author__ = 'fnd212'
__reviewer__ = 'sb5518'

"""
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

"""

from defined_exceptions import *
import sys
import databases_utils
import interface_utils
from results import address_analysis_output, comparative_analysis_output
from addressClass import Address, NoInternetAccess, InvalidGmapsKey
from statistics import CrimesDataFrame, address_analysis
import os


def main():
    # Maximum number of addresses for analysis allowed
    MAX_ADDRESSES = 10

    interface_utils.display_welcome_screen()

    # Load DB of crimes. If Database is not clean, the program will clean it and the user will have the option to save it
    crimes_database = databases_utils.get_crimes_db()
    os.system('clear')  

    # Ask for user to choose a range of years and filter the Database accordingly
    crimes_database = databases_utils.filter_db_by_timeframe(crimes_database)

    # Ask for user to choose one or more types of crime and filter the Database accordingly
    crimes_database = databases_utils.filter_db_by_crime(crimes_database)

    # Create an instance of the CrimesDataFrame class with the filtered Database. This class is in charge of Statistics
    crimes_database = CrimesDataFrame(crimes_database)

    # Create lists to save addresses and addresses names of interest
    user_addresses = []
    user_addresses_names = []

    # Create interface Options
    interface_options = ['Add another address','Delete saved address',
                        'View saved address', 'Comparative analysis','Quit']
    option = 'Add another address'

    # Main loop of the program. It will ask for user input and show maps and analyses until 'Quit' is introduced
    while 1:

        if (not user_addresses) or option == 'Add another address':

            try:
                # Create an instance of Address class. It will ask user to input an address, validate it through
                # Google Maps, and calculate/save several attributes of that address.
                address = Address()

            except NoInternetAccess:
                print('No Internet connection found')
                if interface_utils.yesno_question('Continue?'):
                    address = None # Continue with the normal loop without saving the address
                else:
                    raise QuitProgram    

            # Create a District Heat Map with maps_builder class and show it.
            if address:
                interface_utils.computing_statistics_message()
                address.summary = address_analysis(crimes_database, address)
                address_analysis_output(address, crimes_database)
                

            # User will have the option to save/discard the address after reviewing the Map and Statistics.
            if interface_utils.yesno_question('Keep this address for comparative analysis?'):
                if len(user_addresses) == MAX_ADDRESSES:
                    print 'Maximum number of addresses to save reached, delete one location before adding a new address'
                else:
                    if address not in user_addresses:
                        user_addresses.append(address)
                        user_addresses_names.append(address.formatted_address)

        # This option will allow the user to review the Map and Stats of an address that was saved.
        elif option == 'View saved address':
            option = interface_utils.get_options_from_user(user_addresses_names + ['Back'], multiple=False)

            if option != 'Back':
                address = user_addresses[user_addresses_names.index(option)]
                interface_utils.computing_statistics_message()
                address_analysis_output(address, crimes_database)                

        # This option will allow the user to delete one of the saved addresses.
        elif option == 'Delete saved address':
            option = interface_utils.get_options_from_user(user_addresses_names + ['Back'], multiple=False)
            if option != 'Back':
                user_addresses.pop(user_addresses_names.index(option))
                user_addresses_names.pop(user_addresses_names.index(option))

        # This option will create a comparative Map and statistics to analyze and compare the saved addresses.
        elif option == 'Comparative analysis':
            comparative_analysis_output(crimes_database, user_addresses)


        # This option is the only way to end the loop and finish the program
        elif option == 'Quit':
            raise QuitProgram

        # If user_addresses is empty start the loop again directly to ask for an address
        # If there are addresses in user_addresses, offer options on how to continue
        if user_addresses:
            option = interface_utils.get_options_from_user(interface_options, multiple=False)



if __name__ == '__main__':    
    try:
        main()

    except KeyboardInterrupt:
        #Implementation decision, CTRL+C stops and quits the program. 
        pass        

    except QuitProgram:
        #Quit program. 
        print('Finishing program...')
        sys.exit(0)

    except FatalError, exception:
        print(exception.message)
        sys.exit(1)

    except InvalidGmapsKey as e:
        print str(e)
        print('Fatal Error: Please get a valid key for gmaps API')
        sys.exit(1)

