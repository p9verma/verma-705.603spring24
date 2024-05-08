from copy import deepcopy
import numpy as np

class Reviews_Dataset():
    
    def __init__(self, data):
        df = deepcopy(data)
        # 80% train, 10% valid, 10% test
        self.train, self.validate, self.test = np.split(df.sample(frac=1, random_state=42), [int(.8*len(df)), int(.9*len(df))])
        
    def get_training_dataset(self):
        return self.train
    
    def get_testing_dataset(self):
        return self.test
    
    def get_validation_dataset(self):
        return self.validate