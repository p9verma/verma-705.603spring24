import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import random_noise

''' 
This class takes in an image and an augmentation type to output the detections found and confidence scores for each augmentation iteration.
'''
class ObjectDetection:
    '''
    The init method initializes the class and runs most of the calculations. The provided yolo model is used with coco class names to find objects in an image.
    '''
    def __init__(self, image, augmentation):
        self.augmentation = augmentation
        self.net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        self.original_image = cv2.imread(image)
        self.classes = None
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.augmented_images = self.augment(self.original_image)
        self.confidences = []
        self.objects_detected = []
        for augmented_image in self.augmented_images:
            blob = cv2.dnn.blobFromImage(augmented_image, 0.00392, (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.net.getUnconnectedOutLayersNames())
            max_confidence = 0
            objects = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > max_confidence:
                        max_confidence = confidence
                        object_name = self.classes[class_id]
                        objects.append((object_name, max_confidence))
            self.objects_detected.append(objects)
            self.confidences.append(max_confidence)
        self.plot_confidences(self.confidences)

    '''
    The augment method performs iterative augmentation experiments based on the augmentation inputted. it returns an array of augmented images to be used for detection.
    '''
    def augment(self, image):
        if self.augmentation == 'size':
            return [cv2.resize(image, size) for size in [(100, 100), (250, 250), (350, 350), (400, 400), (2000, 2000), (2229, 3344)]]
        elif self.augmentation == 'gaussian':
            return [cv2.add(image, self.get_gaussian_noise(image, std_dev)) for std_dev in [0.1, 0.2, 0.4, 1.0, 1.5, 2.0, 2.5]]
        elif self.augmentation == 'rotation':
            return [cv2.rotate(image, angle) for angle in [30, 60, 90, 180, 240, 270, 300, 360]]

    '''
    This is a helper method to get the gaussian noise for an image based on standard deviation inputs.
    '''
    def get_gaussian_noise(self, image, std_dev):
        gauss = np.random.normal(loc=1, scale=2, size=(image.shape[0], image.shape[1], image.shape[2]))
        gauss = gauss.reshape(image.shape).astype('uint8')
        return gauss

    '''
    This is a helper function to plot the confidences. The degradation point based on image augmentations in confidence can be observed on these charts.
    '''
    def plot_confidences(self, confidences):
        plt.plot(range(1, len(confidences) + 1), confidences)
        plt.xlabel('Augmentation')
        plt.ylabel('Yolo Confidence')
        plt.title('Yolo Confidence v ' + self.augmentation + ' augmentation')
        plt.show()