import os 
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix, matthews_corrcoef
from imblearn.metrics import specificity_score, sensitivity_score
import numpy as np
import matplotlib.pyplot as plt

class Metrics():
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
        
        with open(os.path.join(filepath,'report.txt'), 'w+') as f:
            f.write("Confusion matrix: \n" + str(confusion_matrix(y_label, y_prediction)))
            f.write("\n\nClassification report: \n" + classification_report(y_label, y_prediction))
            f.write("MCC: " + str(matthews_corrcoef(y_label, y_prediction)))
        
    def run(self, y_prediction, y_label):
        # Generate Report
        # precision, recall, fscore, support = score(y_label, y_prediction)
        
        # print("Model Results: \n")
        # print(f"Precision: ", precision_score(y_label, y_prediction, average="macro"))
        # print(f"Recall: ", recall_score(y_label, y_prediction, average="macro"))
        # print(f"Sensitivity: ", sensitivity_score(y_label, y_prediction, average="macro"))
        # print(f"Specificity: ", specificity_score(y_label, y_prediction, average="macro"))
        # print(f"MCC: ", matthews_corrcoef(y_label, y_prediction))
        # # Generate Figures
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
        y_prediction_binary = [1 if label == 'positive' else 0 for label in y_prediction]
        y_label_binary = [1 if label == 'positive' else 0 for label in y_label]
        
        # Calculate metrics
        precision = precision_score(y_label_binary, y_prediction_binary)
        recall = recall_score(y_label_binary, y_prediction_binary)
        accuracy = accuracy_score(y_label_binary, y_prediction_binary)
        f1 = f1_score(y_label_binary, y_prediction_binary)
        mcc = matthews_corrcoef(y_label_binary, y_prediction_binary)
        
        # Print metrics
        print("Precision:", precision)
        print("Recall:", recall)
        print("Accuracy:", accuracy)
        print("F1 Score:", f1)
        print("MCC:", mcc)