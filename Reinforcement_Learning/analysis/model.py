import numpy as np
import pandas as pd
import random
from copy import deepcopy
import data_pipeline
from data_pipeline import ETL_Pipeline
import dataset
from dataset import Email_Dataset
from metrics import Metrics

'''
This class constructs the model and handles the necessary logic to take raw input data, and produce an output.
'''
class Q_learner_Model():

    '''
    The init function initializes the class. If we already have a trained q_table and want to run metrics, the parameters q_table_trained (numpy array) , userbase (pandas dataframe), sent_emails (pandas dataframe), and responded (pandas dataframe) can be specified. If not, the can be marked 'None'.
    '''
    def __init__(self, q_table_trained, userbase, sent_emails, responded):
        self.q_table_trained = q_table_trained
        self.userbase = userbase
        self.sent_emails = sent_emails
        self.responded = responded

    '''
    This function handles the input data loading, transforming, processing, and model training.
    The model (q-table) is also saved to an output file for reference.
    The processed dataframe and trained q_table are returned.
    '''
    def reinforcement_solution(self, episodes, epsilon, alpha, gamma, userbase_filename, responded_filename, sent_emails_filename):
        # extract data
        pipeline = ETL_Pipeline()
        self.responded = pipeline.extract(responded_filename)
        self.userbase = pipeline.extract(userbase_filename)
        self.sent_emails = pipeline.extract(sent_emails_filename)
        # transform data
        self.userbase = pipeline.transform(self.userbase)
        # Q-learning algorithm
        number_of_actions = 3  # Number of subject lines˜
        self.q_table = np.zeros((192, 3)) # Initialize q_table
        self.age_labels = list(self.userbase['Age_Group'].unique())
        self.tenure_labels = list(self.userbase['Tenure_Group'].unique())
        for _ in range(episodes):
            print("Running episode ", _)
            # Pick random user and get data
            index = random.randint(0, len(self.userbase) - 1) 
            age_group = self.userbase.iloc[index]['Age_Group']
            tenure_group = self.userbase.iloc[index]['Tenure_Group']
            gender_code = self.userbase.iloc[index]['Gender_code']
            type_code = self.userbase.iloc[index]['Type_code']
            # Get specific state's index in table
            state = (self.tenure_labels.index(tenure_group) * 24 + self.age_labels.index(age_group) * 4 + gender_code * 2 + type_code)
            # explore v exploit 
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 2)  #Explore
            else:
                action = np.argmax(self.q_table[state])  #Exploit
            # Determine reward
            customer_id = self.userbase.iloc[index]['Customer_ID']
            sent_date = self.sent_emails.iloc[index]['Sent_Date']
            responded_success = self.responded.apply(lambda x: x['Customer_ID'] == self.userbase.iloc[index]['Customer_ID'] and x['Responded_Date'] == self.sent_emails.iloc[index]['Sent_Date'], axis=1)
            # if customer opened email on the same day it is sent, we have an optimal action
            if responded_success.any(): 
                reward = 100
            # Default action is customer opening an email sent
            elif self.sent_emails.iloc[index]['Customer_ID'] in self.responded['Customer_ID'].values: 
                reward = 10
            # no reward for email that is not opened
            else: 
                reward = 0 
            # Update q-table
            self.q_table[state, action] = (1-alpha) * self.q_table[state, action]+alpha*(reward+gamma*action - self.q_table[state, action])
            alpha = initial_alpha / episode
        np.save('q_table_' + episodes + '_' + epsilon + '_' + alpha + '_' + gamma + '.npy', self.q_table)
        self.q_table_trained = q_table
        return self.userbase, self.q_table

    '''
    The test function runs the q_table and outputs metrics and generates a report. It returns both predicted and ground truth values.
    '''
    def test(self, df):
        print(f'Generating predictions...')
        self.age_labels = list(self.userbase['Age_Group'].unique())
        self.tenure_labels = list(self.userbase['Tenure_Group'].unique())
        # if self.q_table_trained.size is None:
        y_prediction = []
        for index,_ in df.iterrows():
            if index%10000 == 0: print(f"Generating actions... currently at index ", index)
            age_group = df.iloc[index]['Age_Group']
            tenure_group = df.iloc[index]['Tenure_Group']
            gender_code = df.iloc[index]['Gender_code']
            type_code = df.iloc[index]['Type_code']
            state = (self.tenure_labels.index(tenure_group) * 24 + self.age_labels.index(age_group) * 4 + gender_code * 2 + type_code)
            y_prediction.append(np.argmax(self.q_table_trained[state])+1)
        # return y_prediction
        print(f'Done generating predictions.')
        true_actions = []
        print(f'Getting ground truth array...')
        for index, row in df.iterrows():
            customer_id = row['Customer_ID']
            age_group = row['Age_Group']
            tenure_group = row['Tenure_Group']
            gender_code = row['Gender_code']
            type_code = row['Type_code']
            state = (self.tenure_labels.index(tenure_group) * 24 + self.age_labels.index(age_group) * 4 + gender_code * 2 + type_code)
            sent_date = self.sent_emails.iloc[index]['Sent_Date']
            responded_success = self.responded.apply(lambda x: x['Customer_ID'] == customer_id and x['Responded_Date'] == sent_date, axis=1)
            if responded_success.any():
                actions.append(self.responded[responded_success]['SubjectLine_ID'].iloc[0])
            else:
                true_actions.append(1)
        print(f'Done getting ground truth.')
        metric = Metrics()
        print(f'Running metrics...')
        metric.run(y_prediction, true_actions)
        metric.generate_report(y_prediction, true_actions)
        print(f'Done!')
        return y_prediction, true_actions

    '''
    The predict function takes in inputs and predicts the best action.
    '''
    def predict(self, input):
        self.age_labels = list(self.userbase['Age_Group'].unique())
        self.tenure_labels = list(self.userbase['Tenure_Group'].unique())
        return np.argmax(self.q_table_trained[(self.tenure_labels.index(input['Tenure_Group']) * 24 + self.age_labels.index(input['Age_Group']) * 4 + input['Gender_code'] * 2 + input['Type_code'])])+1
    