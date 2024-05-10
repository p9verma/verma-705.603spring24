from flask import Flask, request, jsonify
from model import Q_learner_Model
import numpy as np
import pandas as pd

app = Flask(__name__)
model = Q_learner_Model(np.load('q_table_1000_0.6_0.6.npy'), pd.read_csv('users_processed.csv'), pd.read_csv('sent_emails.csv'), pd.read_csv('responded.csv'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    result = model.predict(data)
    result = int(result)
    return jsonify({'Best action': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
