import datetime
from datetime import date
import pandas as pd
from copy import deepcopy
'''
The ETL pipeline class is used to transform the data using the knowledge discovered in your Exploratory Data Analysis.
'''
class ETL_Pipeline:
    '''
    The extract function takes 'filename' as a parameter indicating the .csv file carrying data we are looking to extract.
    Returns: dataframe 
    '''        
    def extract(self, filename):
        df = pd.read_csv(filename)
        return df
    '''
    The transform function contains all the processes needed to clean, process, and prepare the data for modeling.
    Params:
    df (pandas dataframe): the extracted dataframe from .csv input file

    Returns:
    df_processed (pandas dataframe): the processed dataframe
    '''        
    def transform(self, df):
         df_processed = deepcopy(df[['rating', 'review_title', 'text', 'helpful_vote', 'average_rating']]) # only add relevant features to processed dataset
         return df_processed[df_processed['text'].notnull()] # data cleansing to ensure no null values can be sent to model
    '''
    The load function contains the processes to write the pre-processed dataset to a specified .csv file using the pandas 'to_csv()' function,. 
    '''
    def load(self, df):
        df.to_csv('reviews_processed.csv', index=False)
        return df
