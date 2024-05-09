import os 
from sklearn.metrics import roc_curve, auc, precision_score, recall_score, matthews_corrcoef
import numpy as np
import matplotlib.pyplot as plt
import metrics_mAP
from metrics_mAP import calculate_precision_recall_curve, calculate_map_11_point_interpolated
from sklearn.metrics import classification_report
import cv2 as cv2
import matplotlib.pyplot
import matplotlib.patches

class Metrics:

    '''
    This function is a predefined helper function that I came accross during my metrics research. 
    The function is able to take in a ground truth and predicted bounding box and output the IOU, intersection, and union.
    
    Reference: https://blog.paperspace.com/mean-average-precision/
    '''
    def intersection_over_union(self, gt_box, pred_box):
        inter_box_top_left = [max(gt_box[0], pred_box[0]), max(gt_box[1], pred_box[1])]
        inter_box_bottom_right = [min(gt_box[0]+gt_box[2], pred_box[0]+pred_box[2]), min(gt_box[1]+gt_box[3], pred_box[1]+pred_box[3])]
    
        inter_box_w = inter_box_bottom_right[0] - inter_box_top_left[0]
        inter_box_h = inter_box_bottom_right[1] - inter_box_top_left[1]
    
        intersection = inter_box_w * inter_box_h
        union = gt_box[2] * gt_box[3] + pred_box[2] * pred_box[3] - intersection
        
        iou = intersection / union
    
        return iou, intersection, union

    
    '''
    This function generates a report in a .txt file format in a directory called `results`
    param y_prediction (array): model output
    param y_label (array): ground truth 
    '''
    def generate_report(self, y_prediction, y_label):
        # print("cwd: ",os.getcwd())
        filepath = os.path.join(os.getcwd(),'results')
        print("Creating report.txt file at ", filepath)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        
        sum = 0
        for i in range(len(y_prediction)):
            iou, intersect, union = self.intersection_over_union(y_label[i], y_prediction[i])
            # print(iou)
            sum = sum + iou
            
        with open(os.path.join(filepath,'report.txt'), 'w+') as f:
            f.write("\n\nAverage IOU for all bounding boxes: \n" + str(sum/i))
    '''
    This function outputs metrics about the model performance
    param y_prediction (array): model output
    param y_label (array): ground truth 
    '''
    def run(self, y_prediction, y_label):
        # Generate Report
        print("Model Results: \n")
        # map_value = self.calculate_map(y_label, y_prediction)
        # 
        sum = 0
        for i in range(len(y_prediction)):
            iou, intersect, union = self.intersection_over_union(y_label[i], y_prediction[i])
            print(iou)
            sum = sum + iou
        print("Average IOU for all bounding boxes: ", sum/i)
                # Generate Figures
        # fpr, tpr, thresholds = roc_curve(y_label, y_prediction)
        # roc_auc = auc(fpr, tpr)
        # plt.figure()
        # plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        # plt.plot([0, 1], [0, 1])
        # plt.xlim([0.0, 1.0])
        # plt.ylim([0.0, 1.05])
        # plt.xlabel('False Positive Rate')
        # plt.ylabel('True Positive Rate')
        # plt.title('ROC Curve')
        # plt.legend(loc="lower right")
        # plt.show()

