from copy import deepcopy
import numpy as np

    '''
    The 'Object_Detection_Datase()' class contains all processes needed to split a dataset into training, testing, and evaluation data.
    '''
class Object_Detection_Dataset:
    '''
    The class initializes and splits data into training, testing, and validation split. 
    Params:
    data (pandas dataframe): data to be split

    Returns intialized Fraud_Dataset class.
    '''
    def __init__(self, data):
        self.data = deepcopy(data)
        # 80% train, 10% valid, 10% test
        self.train, self.validate, self.test = np.split(self.data.sample(frac=1, random_state=42),
                                                         [int(.8*len(self.data)), int(.9*len(self.data))])
    '''
    get_training_dataset() is a getter method to get the training dataset
    '''    
    def get_training_dataset(self):
        return self.train
    '''
    get_testing_dataset() is a getter method to get the testing dataset
    '''   
    def get_testing_dataset(self):
        return self.test
    '''
    get_validation_dataset() is a getter method to get the validation dataset
    '''
    def get_validation_dataset(self):
        return self.validate
