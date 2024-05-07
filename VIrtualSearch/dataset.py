from copy import deepcopy
import numpy as np

class Object_Detection_Dataset:
    
    def __init__(self, data):
        self.data = deepcopy(data)
        # 80% train, 10% valid, 10% test
        self.train, self.validate, self.test = np.split(self.data.sample(frac=1, random_state=42),
                                                         [int(.8*len(self.data)), int(.9*len(self.data))])
        
    def get_training_dataset(self):
        return self.train
    
    def get_testing_dataset(self):
        return self.test
    
    def get_validation_dataset(self):
        return self.validate