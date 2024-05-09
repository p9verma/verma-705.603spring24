import sys
import cv2
import numpy as np
from metrics import Metrics
import data_pipeline
from data_pipeline import ETL_Pipeline
import numpy as np

'''
This class constructs the model and handles the necessary logic to take raw input data, and produce an output.
'''
class Object_Detection_Model():
    '''
    This method intializes the class. An weights and config path are used to instantiate the model.
    Returns an initialized model class instance.
    '''
    def __init__(self, weights_path, config_path):
        self.model = cv2.dnn.readNet(weights_path, config_path)
        self.classes = ['license_plate']
    '''
    The test method accepts images and ground truth bounding boxes as inputs to predict and run the metrics
    pipeline on predictions. The method returns the array of bounding box predictions.
    '''
    def test(self, images, truth): #no training in this model, requires inputting actual labels for metrics.
        y_prediction = []
        for i, image_path in images.iterrows():
            image = cv2.imread(image_path[0])
            str = self.predict(image)
            parts = str.strip('<>').split('> <')
            if len(parts) < 2: 
                label = ""
                bbox = [0,0,0,0]
            else:
                label = parts[0]
                bbox = list(map(float, parts[1].strip('[]').split(',')))
            y_prediction.append(bbox)
        metric = Metrics()
        # metric.run(np.array(y_prediction), np.array(truth))
        metric.generate_report(np.array(y_prediction), np.array(truth))
        return y_prediction

    '''
    The predict method takes in an input image and runs predictions on it in order to detect.
    It returns a string output: "<class> <bounding_box_parameters>"
    '''
    def predict(self, input_image):
        layer_name = self.model.getLayerNames()
        output_layer = [layer_name[i - 1] for i in self.model.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(1, 3))
        blob = cv2.dnn.blobFromImage(input_image, 0.00392, (416, 416), swapRB=True)
        self.model.setInput(blob)
        outs = self.model.forward(output_layer)
        confidence_threshold = 0.5
        
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > confidence_threshold:
                    # Object detection
                    center_x = int(detection[0] * input_image.shape[1])
                    center_y = int(detection[1] * input_image.shape[0])
                    w = int(detection[2] * input_image.shape[1])
                    h = int(detection[3] * input_image.shape[0])
                    # Rectangle coordinates
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Apply non-max suppression to eliminate redundant overlapping bounding boxes
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        output_string = ""
        label = ""
        x,y,w,h = 0, 0, 0, 0
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = self.classes[class_ids[i]]
                confidence = confidences[i]
        # print(label, x,y,w,h)
        return f"<{label}> <{[x,y,w,h]}>"
