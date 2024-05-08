from flask import Flask, request, jsonify
from reviews_model import Reviews_Model

app = Flask(__name__)
model = Reviews_Model()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    result = model.predict(data)
    return jsonify({'sentiment': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
