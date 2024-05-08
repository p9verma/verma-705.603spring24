import datetime
from datetime import date
import pandas as pd
from copy import deepcopy

class ETL_Pipeline:
        
    def extract(self, filename):
        df = pd.read_csv(filename)
        return df
        
    def transform(self, df):
         df_processed = deepcopy(df[['rating', 'review_title', 'text', 'helpful_vote', 'average_rating']])
         return df_processed[df_processed['text'].notnull()]

    def load(self, df):
        df.to_csv('reviews_processed.csv', index=False)
        return df