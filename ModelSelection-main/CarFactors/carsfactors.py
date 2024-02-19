# Multiple Linear Regression

# Importing the libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class carsfactors:
    
    def __init__(self):
        self.modelLearn = False
        self.stats = 0

    def model_learn(self):

        
        # Importing the dataset into a pandas dataframe
        df = pd.read_csv("cars.csv")
        # note your selected features to address the concern.  Select "useful" columns.  You do not need many.
        df_useful = df[["body_type", "transmission", "color", "duration_listed"]]
        
        #Remove Unwanted Columns
         
        # Seperate X and y (features and label)  The last feature "duration_listed" is the label (y)
        # Seperate X vs Y
        X = df_useful.loc[:, df_useful.columns != "duration_listed"]
        y = df_useful["duration_listed"]
         
        # Do the ordinal Encoder for car type to reflect that some cars are bigger than others.  
        # This is the order 'universal','hatchback', 'cabriolet','coupe','sedan','liftback', 'suv', 'minivan', 'van','pickup', 'minibus','limousine'
        # make sure this is the entire set by using unique()
        # create a seperate dataframe for the ordinal number - so you must strip it out and save the column
        # make sure to save the OrdinalEncoder for future encoding due to inference
        ordinal_labels = ['universal', 'hatchback', 'cabriolet', 'coupe', 'sedan', 'liftback', 'suv', 'minivan', 'van', 'pickup', 'minibus', 'limousine']
        # print(df_useful["body_type"].unique())
        encoder = OrdinalEncoder(categories=[ordinal_labels])
        self.body_type_encoder = encoder
        
        df['body_type_encoded'] = encoder.fit_transform(df[['body_type']])
        # print(df['body_type_encoded'])
        # Do onehotencoder the selected features - again you need to make a new dataframe with just the encoding of the transmission
        # save the OneHotEncoder to use for future encoding of transmission due to inference
        encoder = OneHotEncoder(sparse_output=False)
        self.transmission_encoder = encoder
        
        onehot_transmission = encoder.fit_transform(df[["transmission"]])
        # Do onehotencoder for Color
        # Save the OneHotEncoder to use for future encoding of color for inference
        encoder_color = OneHotEncoder(sparse_output=False)
        onehot_color = encoder_color.fit_transform(df[["color"]])
        self.color_encoder = encoder_color
        # combine all three together endocdings into 1 data frame (need 2 steps with "concatenate")
        # add the ordinal and transmission then add color
        df_onehot_color = pd.DataFrame(onehot_color, columns=encoder_color.get_feature_names_out(['color']))
        df_onehot_transmission = pd.DataFrame(onehot_transmission, columns=encoder.get_feature_names_out(['transmission']))
        df_processed = pd.concat([df_onehot_color, df_onehot_transmission, pd.DataFrame(df[['body_type_encoded', 'duration_listed']])], axis=1)
        # print(df_processed.head())
        
        # then dd to original data set
        
        #delete the columns that are substituted by ordinal and onehot - delete the text columns for color, transmission, and car type 

        # Splitting the dataset into the Training set and Test set 
        X = df_processed.loc[:, df_processed.columns != "duration_listed"]
        y = df_processed[["duration_listed"]]
        # print(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Feature Scaling - required due to different orders of magnitude across the features
        # make sure to save the scaler for future use in inference
        scaler = StandardScaler()
        
        self.scaler = scaler
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Select useful model to deal with regression (it is not categorical for the number of days can vary quite a bit)
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        self.stats = self.model.score(X_train, y_train)
        self.modelLearn = True
        

    # this demonstrates how you have to convert these values using the encoders and scalers above (if you choose these columns - you are free to choose any you like)
    def model_infer(self,transmission, color, bodytype):
        if(self.modelLearn == False):
            self.model_learn()
        print(self, bodytype)
        #convert the body type into a numpy array that holds the correct encoding
        carTypeTest = self.body_type_encoder.transform(np.array(bodytype).reshape(-1, 1))
        carTypeTest = np.array(carTypeTest)
 
        #convert the transmission into a numpy array with the correct encoding
        carHotTransmissionTest = self.transmission_encoder.transform(np.array(transmission).reshape(-1, 1))
        carHotTransmissionTest = np.array(carHotTransmissionTest)
        
        #conver the color into a numpy array with the correct encoding
        carHotColorTest = self.color_encoder.transform(np.array(color).reshape(-1, 1))
        carHotColorTest = np.array(carHotColorTest)

        #add the three above
        total = np.concatenate((carTypeTest,carHotTransmissionTest), 1)
        total = np.concatenate((total,carHotColorTest), 1)
        
        # build a complete test array and then predict
        #othercolumns = np.array([[odometer ,year, price]])
        #totaltotal = np.concatenate((total, othercolumns),1)

        #must scale
        attempt = self.scaler.transform(total)
        
        #determine prediction
        y_pred = self.model.predict(attempt)
        return str(y_pred)
        
    def model_stats(self):
        if(self.modelLearn == False):
            self.model_learn()
        return str(self.stats)
