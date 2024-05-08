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

class Reviews_Model():
    
    def __init__(self):
        nltk.download('vader_lexicon')
        self.model = SentimentIntensityAnalyzer()
    
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

    def predict(self, data):
        prediction = self.model.polarity_scores(str(data['text']))
        if prediction['compound'] >= 0.05:
            return 'positive'
        elif prediction['compound'] <= -0.05:
            return'negative'
        else:
            return 'neutral'
            