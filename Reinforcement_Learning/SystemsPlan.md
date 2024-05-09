
# MOTIVATION (Why's)
## **Why are we solving this problem?**

### <u>Problem Statement</u>

Email campaigns are a powerful modern-day marketing tool. However, with exponentially increasing levels of virtual information and clutter a person receives daily, most often emails can get lost or ignored amongst the myriad others we receive. Thus, email campaigns must be carefully curated to maximize their impact. 

### <u>Value Proposition</u>

The benefits of creating a system to maximize email campaigns is that it will allow for marketing efforts including financial, timely, technical, data storage, and service investements to be maximized and not wasted. Additionally, a more curated method of sendin out emails should lessen the clutter and irrelevant mail sent to someone not likely to address it. This promotes efficiency for the marketer and increases satisfaction for the receptor of the email campaign.

## **Why is our solution a viable one?**

An ML solution fits this problem because it is hard to encode in software and algorithmically define.  Patterns in the data that indicate whether a user is likely to respond to an email may be convoluted in complex mathematical regression or correlation amongst multiple factors or features. Further, the amount of possible users based on feature (considered the *states* in q-learning) are large and can grow to be immense. These states can then be tedious to analyze without the use of advanced ML methodologies. It is beneficial to encode the mathematial Q-learning equation in software to save time. We can tolerate a healthy level of mistakes in this system, as ultimately, sending the wrong email to the wrong user is not life-threatening or even very damaging to the sender's business. However, marketing is a costly and time-labrious effort, so the model should aim for optimal resuls.
 
# REQUIREMENTS (What's)
## **SCOPE:**

### <u>What are our goals?</u>

One of the main goals of this system is to populate a q-table using the q-learning equaion based on features extracted from the Kaggle datasets. This table will be optimized to then return the best acion to take for a given state or more specifically, the best email campaign subject line to send for a given user "type". This is a systematic goal that will help the system optimally curate email campaigns.
 
### <u>What are the success criteria?</u>

The success criteria in this system will be the resultant conversion rate or rate of reponse in the real environment. A success or "response" in this system is defined as an email that is opened on the same day it is sent. Tests performed on labeled data will determine the model's performance for reponse rate pre-deployement. 
 
## **REQUIREMENTS:**

### <u>What are our (system) Assumptions?</u>
- The input data is accurately and represents all the states possibilities.
- The users response likelihood is not significantly impacted by many factors outside of the given dataset.
- There are underlying patterns that can be detected from email data to aid the development of a usable ML model.
 
### <u>What are our (system) Requirements?</u>
- Input email transaction data in a csv format.
- The system must have a reasonable large memory and gpu/cpu operating capability to create q-table for a maximum number of episodes.
- Store and secure input data. The data inputted in this system is highly sensitive and contains PII. it should be protected from breaches or leaks.
 
## **RISK & UNCERTAINTIES:**

### <u>What are the possible harms?, What are the causes of mistakes</u>

The possible harms in this system can be financial, time, and storage wastes. When emails are less-than-optimally sent, users will ignore them and the sender will have wasted their time and monetary efforts on marketing to that user. When too many unsolicited and irrelevant emails are sent, the user may block the sender altogether, leading to a loss of business for the sender. A major case of errors or mistakes may arise from incorrect choice of data features that are collected. We do not know what other factors may have a large impact on the email response rate. However, this can be readily remedied with a market or user survey to calibrate data collection focus and processes.
 
# IMPLEMENTATION (How's)
## **DEVELOPMENT:**
### <u>Methodology</u>
The ETL_Pipeline class is defined in **[data_pipeline](./data_pipeline.py)**. This class contains three main functional methods supporting ETL processing: extract(), transform(), and load().

Extract(): This function takes in a parameter called *filename* indicating the .csv file carrying data and extracts into a dataframe. This function returns the dataframe.

Transform(): This function accepts a dataframe and input and processes it to create new features. These features are extracted based on findings from data analysis performed in **[epxloratory_data_analysis.ipynb](analysis/epxloratory_data_analysis.ipynb)**. The new feature applied to transform the incoming email data are
1. Age_group: the age group of the user (based on defined bins on 'Age')
2. Tenure_group: the tenure group of the user (based on defined bins on 'Tenure')
3. Gender_code: one-hot-encoded Gender feature
4. Type_code: one-hot-encoded type feature

This function contains all the processes needed to clean, process, and prepare the data for modeling.

Load(): This function accepts a dataframe and saves it to a csv file titled *emails_processed.csv*

The Email Dataset class defined in **[dataset.py](./dataset.py)** takes in a dataframe upon instantiation and splits it into a training, testing and validation set using an 80%, 10%, 10% split respectively. The splits are accesible via helper methods in the class: *get_training_dataset()*, *get_testing_dataset()*, and *get_validation_dataset()*.

The Metrics class defined in **[metrics.py](metrics.py)** generates a report and outputs metrics for model evaluation given a set of prediction and truth values. The metrics used are response rate.

Deployement Strategy: The system is dokerized using **[ml_microservice.py](analysis/ml_microservice.py)**, the given video streaming code. Using this flask app, given an input state, the pretrained model (the q-table) output the best action to take (the best subject line to send).

### <u>High-level System Design</u>

At a high level, this system stores data in a csv format, processes and trains a q-learning model with it, and predicts the best action to take for a given state. In this system, the integral component of reinforcement Q-learning are defined as:

**States**: All combinations of Age group ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70'] , tenure group ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40'] , gender [M, F] , and type [B (business), C (consumer)]. There are 6x8x2x2=192 total states.

**Actions**: Subject line to send [1, 2, or 3]. There are three total actions.

**Rewards**: -10 if no response and 10 if responded. A response is defined as the opened_date being the same as sent_date.

Modular code breaks up the input data and pipelines process the data, and train the model. Using the q-learning component definitions above, a q-table is created based on an inputted number of training *episodes*. The dockerized system uses the modules and a *predict()* method to output the optimal email subject line to send for an inputted user state (age_group, tenure_group, gender, type). This system can be integrated in larger software to automate the sending of the most optimal emails, or curate email lists for each subject line based on the q_table and user's emails. Both these methods can allow for the most optimal email campaign to be sent with just a few clicks, maximing efficiency and achieving the defined goals.  

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
