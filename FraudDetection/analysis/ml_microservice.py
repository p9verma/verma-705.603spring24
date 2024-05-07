from flask import Flask
from flask import request
import os
# import datetime
import pandas as pd
import joblib
# import pkg_resources
# pkg_resources.require("sklearn==1.3.2")
import sklearn

# import sys
# sys.path.append("Desktop/AI Masters/705.603/workspace/verma-705.603spring24/FraudDetection/data_pipeline.py")
# sys.path.append("Desktop/AI Masters/705.603/workspace/verma-705.603spring24/FraudDetection/data_pipeline.py")
# import model
from model import Fraud_Detector_Model
# import ..data_pipeline
from data_pipeline import ETL_Pipeline

# import logging
from flask import jsonify

app = Flask(__name__)

# Define the route for model inference
@app.route('/predict', methods=['POST'])
def getPredict():
    input_data = request.json
    # logging.debug("Input TESTESTESTESJSON data: %s", input_data)
    features = ['Unnamed: 0', 'zip', 'city_pop', 'is_fraud', 'age', 'hour_of_day', 'is_holiday', 'is_post_holiday', 'is_summer', 'fraud_mean', 'fraud_std', '2.5_std', 'likely_fraudulent_time', 'age_group_18-30', 'age_group_31-40', 'age_group_41-50', 'age_group_51-60', 'age_group_61-70', 'age_group_70+', 'Day of week_Friday', 'Day of week_Monday', 'Day of week_Saturday', 'Day of week_Sunday', 'Day of week_Thursday', 'Day of week_Tuesday', 'Day of week_Wednesday', 'Month_April', 'Month_August', 'Month_December', 'Month_February', 'Month_January', 'Month_July', 'Month_June', 'Month_March', 'Month_May', 'Month_November', 'Month_October', 'Month_September']
    df = pd.DataFrame([input_data])
    print(df.columns)
    transformed_data = pipeline.transform(df)
    transformed_data = transformed_data.fillna(0)
    for feature in features:
        if feature not in transformed_data.columns:
            transformed_data[feature] = 0
    return jsonify(model_rf.predict(transformed_data[features].drop(columns=['is_fraud'], axis=1)))
    
if __name__ == "__main__":
    flaskPort = 8786
    # app.run(debug=True)
    # logging.basicConfig(level=logging.DEBUG)
    # filename = "/Users/punitaverma/Desktop/AI Masters/705.603/workspace/verma-705.603spring24/FraudDetection/transactions.csv"
    model_rf = Fraud_Detector_Model(None, joblib.load('best_trained_model.pkl'))
    pipeline = ETL_Pipeline()
    print('starting server...')
    app.run(host = '0.0.0.0', port = flaskPort)