from flask import Flask
from flask import request
import os

from carsfactors import carsfactors

app = Flask(__name__)

# http://localhost:8786/infer?transmission=automatic&color=blue&odometer=12000&year=2020&bodytype=suv&price=20000

@app.route('/stats', methods=['GET'])
def getStats():
    return str(cf.model_stats())

@app.route('/infer', methods=['GET'])
def getInfer():
    args = request.args
    transmission = args.get('transmission')
    color = args.get('color')
    print("REQ: ", request, "ARGS: ", request.args)
    bodytype = args.get('bodytype')
    return cf.model_infer(transmission, color, bodytype)

@app.route('/post', methods=['POST'])
def hellopost():
    args = request.args
    name = args.get('name')
    location = args.get('location')
    print("Name: ", name, " Location: ", location)
    imagefile = request.files.get('imagefile', '')
    print("Image: ", imagefile.filename)
    imagefile.save('/workspace/Hopkins/705.603Fall2023/workspace/ML_Microservice_Example/image.jpg')
    return 'File Received - Thank you'

if __name__ == "__main__":
    flaskPort = 8080
    cf = carsfactors()
    print('starting server...')
    app.run(host = '0.0.0.0', port = flaskPort)

