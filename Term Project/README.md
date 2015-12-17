

# README  
### DS-GA-1007 Project 
### Team member: Yichen Fan (yf511), Li Ke (lk1818), Kaiwen Liu(kl1405)
======================= 
 
Thank you very much for reading this README file! You will find this very helpful.  
 
The data files of this project are downloaded from Kaggle Competition ‘Rossmann Store Sales’ on the website:

https://www.kaggle.com/c/rossmann-store-sales/data.  
 
Data files description: the train.csv file contains historical data including sales between January 1st, 2013 and July 31st, 2015. The test.csv file contains historical data excluding sales between August 1st, 2015 and September 17th, 2015. The store.csv file contains supplemental information about the stores. 
 
This program predicts the daily sales of the 1115 Rossmann drug stores between August 1st, 2015 and September 17th, 2015, based on the past data. Each store has a unique store ID ranges from 1 to 1115. The following is an instruction to run the program. 
 
First of all, there is an ultimate data cleaning function that takes an hour to run. Therefore, we have created the structured data if the user chooses not to run it again. As a result, the program will ask the user if he wants to run this function, or if he just wants to use our previously structured data. Enter ‘yes’ to run, or enter ‘no’ to use the previously cleaned data. 
 
Secondly, the program asks the user to input a store ID number between 1 and 1115, then it will predict the future daily sales (between Aug 1st, 2015 and Sep 17th, 2015) of this store and save a plot of predicted sales versus dates. Some stores are missing from the test data set, and if the input happens to be one of them, the program will prompt the user for another input. 
 
Thirdly, the program asks if the user wants to see prediction value of sale on a specific date given the store ID number provided in the previous procedure. User can input a date in the format of MMDD. (i.e. 0902)   
 
In the end, the program continues to ask the user to see another store (repeat the second and third procedures). If the user wants to quit the program, then simply type ‘no’ or 'finish' will do the job.


```python

```
