import pandas as pd
import sys
from copy import deepcopy
sys.path.insert(1, '/Users/punitaverma/Desktop/workspace/verma-705.603spring24/Sentiment_Analysis')
import data_pipeline
from data_pipeline import ETL_Pipeline
import dataset
from dataset import Reviews_Dataset
from metrics import Metrics
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

'''
This class constructs the Reviews Model and handles the necessary logic to take raw input data, and produce an output.
'''
class Reviews_Model():
    
    '''
    This method initializes the pre-trained vader sentiment analyzer. 
    '''
    def __init__(self):
        nltk.download('vader_lexicon')
        self.model = SentimentIntensityAnalyzer()
   
    '''
    The test method tests the model performance on a given dataset using the metrics module. 
    
    Sentiment analysis cannot have a ground truth in this case. 
    For that reason, the 'ground truth' is generated using the 'rating' feature in the data. The rationale behind
    this is that the producer of the review and its sentiment quantified the intended sentiment via the rating number.
    This is discussed in the SystemsPlan document further.

    Returns an array of predicted sentiment labels.
    '''
    def test(self, df):
        metric = Metrics()
        y_prediction = []
        for i, row in df.iterrows():
            # print(df.iloc[i,2])
            prediction = self.model.polarity_scores(str(df.iloc[i,2]))
            # if prediction['compound'] 
            if prediction['compound'] >= 0.05:
                label = 'positive'
            elif prediction['compound'] <= -0.05:
                label = 'negative'
            else:
                label = 'neutral'
            y_prediction.append(label)
            df.at[i, 'sentiment'] = label
        # df['sentiment_cat'] = pd.cut(df['sentiment'], bins=[-1, -0.5, 0.5, 1], labels=['negative', 'neutral', 'positive'])
        df['rating_cat'] = pd.cut(df['rating'], bins=[0, 2.5, 3.5, 5], labels=['negative', 'neutral', 'positive'])
        metric.run(df['sentiment'] , df['rating_cat'])
        metric.generate_report(df['sentiment'] , df['rating_cat'])
        return y_prediction
     
    '''
    The predict method is used to predict sentiment of a given input. 

    Params:
    input (array): data representing a review via a row from the master reviews dataframe 

    Returns a string output descibing the review's sentiment.
    '''
    def predict(self, data):
        prediction = self.model.polarity_scores(str(data['text']))
        if prediction['compound'] >= 0.05:
            return 'positive'
        elif prediction['compound'] <= -0.05:
            return'negative'
        else:
            return 'neutral'
            
