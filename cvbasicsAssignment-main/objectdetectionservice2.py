from flask import Flask, request, jsonify
import os
from ObjectDetection import ObjectDetection

app = Flask(__name__)

'''
This Flask app reads in a posted image, runs YOLO on it, and outputs detections and confidence scores based on augmentation experiements. The results can then be parsed to determine the best detections.
'''
@app.route('/detect', methods=['POST'])
def detection():
    image_file = request.files.get('imagefile')

    image_file_path = 'temp_image.jpg'
    image_file.save(image_file_path)
    augmentation_types = ['size', 'gaussian', 'rotation']
    detections = {}
    for augmentation_type in augmentation_types:
        detector = ObjectDetection(image_file_path, augmentation_type)
        confidences = [float(confidence) for confidence in detector.confidences]
        
        detection_results = []
        for objects_detected in detector.objects_detected:
            detection_results.append([(obj_name, float(confidence)) for obj_name, confidence in objects_detected])
        detections[augmentation_type] = {
            'objects': detection_results,
            'confidences': confidences
        }
    os.remove(image_file_path)
    return jsonify(detections)

'''
The app runs on port 8786
'''
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8786)
