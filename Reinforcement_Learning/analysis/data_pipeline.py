import datetime
from datetime import date
import pandas as pd
from copy import deepcopy
'''
The ETL pipeline class is used to transform the data using the knowledge discovered in your Exploratory Data Analysis.
'''
class ETL_Pipeline:
    '''
    The extract function takes 'username' as a parameter indicating the .csv file carrying userbase data we are looking to extract.
    Returns: dataframe 
    '''  
    def extract(self, filename):
        userbase_df = pd.read_csv(filename)
        return userbase_df

    '''
    The transform function contains all the processes needed to clean, process, and prepare the data for modeling.
    Params:
    df (pandas dataframe): the extracted dataframe from .csv input file

    Returns:
    userbase_df (pandas dataframe): the processed dataframe
    '''
    def transform(self, df):
        userbase_df = deepcopy(df)
        
        # New feature: gender_code
        userbase_df['Gender_code'] = [0 if x == 'M' else 1 for x in userbase_df['Gender']]

        # New feature: type_code
        userbase_df['Type_code'] = [0 if x == 'B' else 1 for x in userbase_df['Type']]

        # New feature: age_group
        userbase_df['Age_Group'] = pd.cut(userbase_df['Age'], bins=[0, 20, 30, 40, 50, 60, 70], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '61-70'])

        # New feature: age_group
        userbase_df['Tenure_Group'] = pd.cut(userbase_df['Tenure'], bins=[0, 5, 10, 15, 20, 25, 30, 35, 40], labels=['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40'])

        return userbase_df.drop(columns=['Email_Address', 'Age', 'Tenure', 'Gender', 'Type']).dropna() # Remove unecessary features 

    '''
    The load function contains the processes to write the pre-processed dataset to a specified .csv file using the pandas 'to_csv()' function,. 
    '''
    def load(self, df):
        df.to_csv('users_processed.csv', index=False)
        return df