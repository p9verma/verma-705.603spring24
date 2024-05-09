# MOTIVATION (Why's)
## **Why are we solving this problem?**

### <u>Problem Statement</u>

The Department of Transportation (DoT) has identified the need to modernize toll collection on its highways to improve traffic flow, reduce congestion, and eliminate the need for manual toll collection. To achieve this, the DoT is interested in deploying an Automated License Plate Recognition (ALPR) system that can accurately and efficiently recognize license plates from various states at high speeds, day and night, under different weather conditions. The task at hand is to develop a machine learning-based ALPR system. The first step in this task is configuring a system to read in live video stream and identifiy license plates. 

### <u>Value Proposition</u>

The benefits of creating a system to detect license paltes will allow DoT to enforce traffic regulations and promote safety and law.

## **Why is our solution a viable one?**

An ML solution fits this problem because it is impossible for the human eye to detect license plates at high speed accurately at all times. This task must be automated and tradition non-ML solutions are incapable of the automation. We can tolerate a small degree of mistakes in this system, but ultimately, most license plates must be detected and be correct in order to charge the correct vehicles for tolls and violations.
 
# REQUIREMENTS (What's)
## **SCOPE:**

### <u>What are our goals?</u>

One of the main goals of this system is to capturing images of moving vehicles at toll booths and accurately recognizing and recording their license plates with high accuracy. The model should consider a probability computed from the training-based predictions that will guide the system’s label for the license plate detection bounding box. This is a systematic goal that will help the system correctly apply tolls. The overall system will not be able to ultimately use some contextual or human inputs in all detetections and thus must be robust.
 
### <u>What are the success criteria?</u>

The success criteria in this system will be tests performed on labeled data. Some metrics we can use to evaluate the runtime performance of the system are Intersection-over-union (IOU), average IOU, and Mean Average Precision (mAP). These metrics have been proven to be state-of-the-art for image detection. Specifically, IOU is able to calculate the correct area covered by the predicted bounding boxes for each detection. A good IOU score likes around +0.5. In the real world system, the success criteria is a correct detection most all of the times.
 
## **REQUIREMENTS:**

### <u>What are our (system) Assumptions?</u>
- The input data is live and coming in at all times.
- The objects (license plates) to be detected from images exist on every car.
- The tessaract software used for licensce plate extraction is trained well and optimally.
 
### <u>What are our (system) Requirements?</u>
- The input data is live and coming in via video stream input.
- The system must have a reasonable large memory and gpu/cpu operating capability to correctly identify licensce lates in near real-time.
- Input will come in at high speeds, day and night, under different weather conditions. The system must handle various image qualities then.
 
## **RISK & UNCERTAINTIES:**

### <u>What are the possible harms?, What are the causes of mistakes</u>

The possible harms in this system can be emotional, legal, and financial damage. If a toll is wrongfully charged by the DoT sometimes or often, it can have ramifications on its authority and credibility with the population. The people may lose trust in the public institution. The specific amount of wrongful charges 
 due to incorrect detections will dictate the degree of the damage caused by the system being inaccurate. Some cases of errors or mistakes include the manner in which data is collected for the model. Lapses in video livestream caused by weather or hardware issues may occur. 
 
# IMPLEMENTATION (How's)
## **DEVELOPMENT:**
### <u>Methodology</u>
The ETL_Pipeline class is defined in **[data_pipeline](./data_pipeline.py)**. This class contains three main functional methods supporting ETL processing: extract(), transform(), and load().

Extract(): This function takes in a parameter called *filename* indicating the .csv file carrying data and extracts into a dataframe. This function returns the dataframe.

Transform(): This function accepts a dataframe and input and processes it to create new features. These features are extracted based on findings from data analysis performed in **[epxloratory_data_analysis.ipynb](analysis/epxloratory_data_analysis.ipynb)**. The new feature applied to transform the incoming license plate data is chnaging image to grayscale. In exploratory analysis, it was found that license numbers are identified at a higher accuracy from tesseract in our input data when grayscale is used.

This function contains all the processes needed to clean, process, and prepare the data for modeling.

Load(): This function accepts a dataframe and saves it to a csv file titled *transactions_processed.csv*

The Object Detection Dataset class defined in **[dataset.py](./dataset.py)** takes in a dataframe upon instantiation and splits it into a training, testing and validation set using an 80%, 10%, 10% split respectively. The splits are accesible via helper methods in the class: *get_training_dataset()*, *get_testing_dataset()*, and *get_validation_dataset()*.

The Metrics class defined in **[metrics.py](metrics.py)** generates a report and outputs metrics for model evaluation given a set of prediction and truth values. The metrics used are IoU and mean IoU. (note: I was unable to get mAP working. However, this is another usefule metric as discussed in the success criteria section).

Deployement Strategy: The system is dokerized using **[udp.py](udp.py)**, the given video streaming code. With ffmpeg installed on the user device, a live video stream can be processed. This video should be processed using the ETL_Pipeline and model classes.

### <u>High-level System Design</u>

At a high level, this system stores data in a csv format, processes and trains a model with it, and predicts license detection in real-time. Video input is broken down into image frames with a customizable frams-per-second (fps) parameter. This can be integrated in the UI to adjust input video processing based on traffic and weather conditions. From the frames, license plates (as specified in the **[classes.txt](classes.txt)** file) are detected using the given Yolo model. A constraint is the Yolo model is a robust pre-trained model and was not finetuned here. Future work may involve finetuning the last few layers of the pre-trained weights, applying transfer learning principle to customize the model. Further down the pipeline, these detections should be used with the Google Tesseract, an optical character recognition engine, to get license plate characters for charging.

### <u>Development Workflow</u>

Adopt agile development methodologies for iterative development and continuous improvement.
Establish CI/CD pipelines for automated testing, deployment, and monitoring.
Collaborate closely with domain experts, data scientists, and engineers to iterate on model development and deployment.


## **OPERATIONS:**
### <u>Continuous Deployment</u>
To uphold continuous deployement standards, the model should be updated with more data and improved algorithms as more research is developed on fraud/anomaly detection.

### <u>Post-deployment Monitoring</u>
The model must be monitored in the real world environment based on the metrics report, customer feedback, and financial reports. 
 
### <u>Maintenance</u>
The model must be monitored for any errors or degradations in performance to upkeep maintainence. Additiohnally, new data must be used to train the model periodically to address any model drift that occurs.
 
### <u>Quality Assurance</u>
Quality assurance must be performed by reguarlarly checking metrics and establishing benchmarks for performance to ensure continued quality of the model predictions.
