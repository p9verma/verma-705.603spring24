import datetime
import pandas as pd
import sys
from copy import deepcopy
# sys.path.insert(1, '/Users/punitaverma/Desktop/AI Masters/705.603/workspace/verma-705.603spring24/FraudDetection')
from datetime import date
# import data_pipeline
from data_pipeline import ETL_Pipeline
# import dataset
from dataset import Fraud_Dataset
from metrics import Metrics
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

class Fraud_Detector_Model():
    
    def __init__(self, model, model_trained):
        self.model = model
        self.model_trained = model_trained
       
    def train(self, filename):
        pipeline = ETL_Pipeline()
        print("Loading data...")
        data = pipeline.extract(filename)
        print("Loaded data of length ", len(data))
        print("Transforming data...")
        data = pipeline.transform(data)
        print("Saving data to csv...")
        data = pipeline.load(data)
        print("Finished saving processed data to csv.")
        print(data.head())
        data = pd.read_csv('transactions_processed.csv')
        dataset = Fraud_Dataset(data)
        self.train_set = dataset.get_training_dataset()
        self.test_set = dataset.get_testing_dataset()
        self.valid_set = dataset.get_validation_dataset()
        print("Training data length: ",len(self.train_set))
        print("Testing data length: ",len(self.test_set))
        print("Validation data length: ",len(self.valid_set))
        x = self.train_set.drop(columns=["is_fraud"])
        y = self.train_set["is_fraud"]
        self.model_trained = self.model.fit(x,y)
        return self.model_trained
    
    def test(self):
        metric = Metrics()
        y_prediction = self.model_trained.predict(self.test_set.drop('is_fraud', axis=1))
        metric.run(y_prediction, self.test_set['is_fraud'])
        metric.generate_report(y_prediction, self.test_set['is_fraud'])

    def predict(self, input):
        # input_data = pd.DataFrame([input])
        prediction = self.model_trained.predict(input)
        if prediction == 0:
            return "Not Fraud"
        else:
            return "Fraud"
        