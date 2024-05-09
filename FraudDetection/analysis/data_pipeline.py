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
    This is a helper function to transform the 'dob' feature to 'age_group'. An intermediate step in the transformation is the calcualtion of age, which is aided by this function.
    '''
    def calculate_age(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    '''
    The transform function contains all the processes needed to clean, process, and prepare the data for modeling.
    Params:
    df (pandas dataframe): the extracted dataframe from .csv input file

    Returns:
    df_processed (pandas dataframe): the processed dataframe
    '''
    def transform(self, df):
        df_processed = deepcopy(df)
        
        # New feature: age
        df_processed["age"]=[self.calculate_age(datetime.datetime.strptime(x, '%Y-%m-%d')) for x in df_processed["dob"]]
        
        # New feature: age_group
        bins = [18, 30, 40, 50, 60, 70, 120]
        labels = ['18-30', '31-40', '41-50', '51-60', '61-70', '70+']
        df_processed['age_group'] = pd.cut(df_processed['age'], bins=bins, labels=labels, right=False)
        
        # New features: Day of week, month, and hour of day
        df_processed['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
        
        df_processed['Day of week'] = df_processed['trans_date_trans_time'].dt.day_name()
        df_processed['Month'] = df_processed['trans_date_trans_time'].dt.month_name()
        df_processed['hour_of_day'] = df_processed['trans_date_trans_time'].dt.hour

        # New features: is_holiday, is_post_holiday, is_summer
        df_processed['is_holiday'] = 0
        df_processed['is_post_holiday'] = 0
        df_processed['is_summer'] = 0

        for index, row in df_processed.iterrows():
            row_dt = row['trans_date_trans_time'].strftime('%m-%d')
            if (row_dt >= '01-01') and (row_dt <= '02-28'): 
                df.at[index, 'is_post_holiday'] = 1
            elif (row_dt >= '05-24') and (row_dt <= '09-01'):
                df.at[index, 'is_summer'] = 1
            elif (row_dt >= '11-30') and (row_dt <= '12-31'):
                df.at[index, 'is_holiday'] = 1

        # New feature: is amt within 3 std deviations of category's mean (fraudulent) amount
        fraudulent_data = df_processed[(df_processed['is_fraud'] == 1)]
        non_fraudulent_data = df_processed[(df_processed['is_fraud'] == 0)]
        
        fraudulent_grouped = fraudulent_data.groupby('category')['amt'].agg(['mean', 'std']).reset_index()
        fraudulent_grouped.columns = ['category', 'fraud_mean', 'fraud_std']
        
        non_fraudulent_grouped = non_fraudulent_data.groupby('category')['amt'].agg(['mean', 'std']).reset_index()
        non_fraudulent_grouped.columns = ['category', 'non_fraud_mean', 'non_fraud_std']
        df_processed = df_processed.merge(fraudulent_grouped, on='category', how='left')
        df_processed = df_processed.merge(non_fraudulent_grouped, on='category', how='left')
        df_processed['upper_bound'] = df_processed['non_fraud_mean'] + 2.5 * df_processed['non_fraud_std']
        df_processed['lower_bound'] = df_processed['non_fraud_mean'] - 2.5 * df_processed['non_fraud_std']
        df_processed['2.5_std'] = (df_processed['amt'] >= df_processed['lower_bound']) & (df_processed['amt'] <= df_processed['upper_bound'])
        df_processed['2.5_std'] = df_processed['2.5_std'].astype(int)

        # New feature: does the transaction occur in the most likely hours of fraudulent transactions?
        df_processed['likely_fraudulent_time'] = ((df_processed['hour_of_day'] >= 24 - 22) | (df_processed['hour_of_day'] <= 22))
        df_processed['likely_fraudulent_time'] = df_processed['likely_fraudulent_time'].astype(int)

        # New feature: top 35 jobs with most fraudulent transactions
        top_jobs = df[df['is_fraud'] == 1].groupby('job')['is_fraud'].count().sort_values(ascending=False).head(35)
        df['is_top_job'] = df['job'].apply(lambda x: 1 if x in top_jobs.index.tolist() else 0)
        
        # return dataframe with new features added
        df_processed = pd.get_dummies(df_processed, columns=['age_group', 'Day of week', 'Month'])
        # Remove features that are not pertinent to model training (such as credit_card number. We do not want the model to just learn the credit card numbers of fraudulent transactions. This may cause some data leakage.)
        return df_processed.drop(columns=['lower_bound', 'upper_bound', 'non_fraud_mean', 'non_fraud_std', 'trans_date_trans_time', 'cc_num', 'category', 'amt', 'first', 'last', 'sex', 'street', 'lat', 'long', 'dob', 'trans_num', 'unix_time', 'merchant', 'job', 'city', 'state', 'merch_lat', 'merch_long']).fillna(0) # 
    '''
    The load function contains the processes to write the pre-processed dataset to a specified .csv file using the pandas 'to_csv()' function,. 
    '''
    def load(self, df):
        df.to_csv('transactions_processed.csv', index=False)
        return df
