# MOTIVATION (Why's)
## **Why are we solving this problem?**

### <u>Problem Statement</u>

Fraudulent transactions on credit cards occur when unauthorized purchases are made from a card. These transactions are hard to detect because the attacker assumes the identity of the credit card holder when making the purchase. Fraudulent transactions attack the integrity of the financial institution, the card holder, and the stakeholder providing the goods being purchased. 

### <u>Value Proposition</u>

The benefits of creating a system to detect fraudulent transactions will allow policing of fraud, safeguard the identity of cardholder, promote trust in the financial institution, and facilitate smoother economic transactions for all stakeholders.

## **Why is our solution a viable one?**

An ML solution fits this problem because it is hard to encode in software and algorithmically define. Differences between true and fradulent transactions are subtle and often unclear to the human eye. Patterns in the data that indicate fraud may be convoluted in complex mathematical regression or correlation amongst multiple factors or features. Further, the amount of non-fraudulent transactions greatly outnumbers the amount of fradulent ones. This creates immensely large and unbalanced datasets that can be tedious to analyze without the use of advanced ML methodologies.
    We can tolerate a small degree of mistakes in this system, as ultimately, most credit card fraud is not life-thratening. However, fraud is a costly problem to all parties involved and most true positives must be detected. 
 
# REQUIREMENTS (What's)
## **SCOPE:**

### <u>What are our goals?</u>

One of the main goals of this system is to mark transactions on their likelihood of being fraudulent. The model should consider a probability computed from the training-based predictions that will guide the system’s label for the transaction. This is a systematic goal that will help the user make an informed decision on whether the transaction needs to be inspected and refunded. The overall system will require the user to ultimately use some contextual and human inputs to determine whether the transaction is infact fraudulent - i.e. if the transaction is labelled non-fradulent but occurs in a country where the cardholder was never present, it is likely fraudulent. The goal of the model is to guide in this decision making process.
 
### <u>What are the success criteria?</u>

The success criteria in this system will be tests performed on labeled data. Since the system will perform predictions in an unsupervised environment, it is difficult to get error scores. However, some metrics we can use to evaluate the runtime performance of the system are precision, recall, F1-score, and MCC. These metrics go beyond accuracy to measure the performance of a model in an imabalanced dataset.
 
## **REQUIREMENTS:**

### <u>What are our (system) Assumptions?</u>
- The input data is highly imbalanced.
- There are underlying patterns that can be detected from transaction data to aid the development of a usable ML model.
- There are enough data point with fraudulent and non-fraudulent transactions to train a model. There is sufficient data.
 
### <u>What are our (system) Requirements?</u>
- Input credit card transaction data in a csv format.
- The system must have a reasonable large memory and gpu/cpu operating capability to process complex training methods on large and high-dimensional datasets.
- Store and secure input data. The data inputted in this system may be highly sensitive and should be protected from breaches or leaks. 
 
## **RISK & UNCERTAINTIES:**

### <u>What are the possible harms?, What are the causes of mistakes</u>

The possible harms in this system can be emotional and financial damage. If a fraudulent tranasaction is marked as non-fradulent by the model, the cardholder may lose trust in the financial institution using this model. The specific amount, nature, and recognition of the fraud will dictate the degree of the damage caused by the system being inaccurate. 

Some cases of errors or mistakes include the manner in which data is collected for the model. Inconsistencies or discrepancies in collecting, aggregating, reporting, storing, loading, and processing the data may cause discrepancies and error is the feature extraction, data loading, data massaging, and model creating processes.
 
# IMPLEMENTATION (How's)
## **DEVELOPMENT:**
### <u>Methodology</u>
The ETL_Pipeline class is defined in **[data_pipeline](./data_pipeline.py)**. This class contains three main functional methods supporting ETL processing: extract(), transform(), and load().

Extract(): This function takes in a parameter called *filename* indicating the .csv file carrying data and extracts into a dataframe. This function returns the dataframe.

Transform(): This function accepts a dataframe and input and processes it to create new features. These features are extracted based on findings from data analysis performed in **[exploratory_data_analysis.ipynb](analysis/exploratory_data_analysis.ipynb)**. The new features added are 
1. Age group: the age group of the transaction's card holder (based on 'dob' feature, age is calculated using a helper function)
2. Day of week: the day of the week of transaction date
3. Month: the month of the transaction date
4. Hour of day: the hour of day of the transaction time
5. is_holiday: Did the transaction during the holidays
6. is_post_holiday: Did the transaction occur after the holidays?
7. is_summer: Did the transaction occur in the summer?
8. 2.5_std: is transaction amount within 3 std deviations of category's mean (fraudulent) amount
9. likely_fraudulent_time: did the transaction occur in hour 22 (time most fraudulent transactions occured)
10. is_top_job: Does the transaction cardholder have a job type occuring in the top 35 cardholder jobs with most fraudulent transactions

This function contains all the processes needed to clean, process, and prepare the data for modeling.

Transform(): This function accepts a dataframe and saves it to a csv file titled *transactions_processed.csv*

The Fraud_Dataset class defined in **[dataset.py](./dataset.py)** takes in a datafram upon instantiation and splits it into a training, testing and validation set using an 80%, 10%, 10% split respectively. The splits are accesible via helper methods in the class: *get_training_dataset()*, *get_testing_dataset()*, and *get_validation_dataset()*.

The Metrics class defined in **[metrics.py](metrics.py)** generates a report and outputs metrics for model evaluation given a set of prediction and truth values. 


### <u>High-level System Design</u>

At a high level, this system stores data in a csv format, processes and trains a model with it, and predict fraud in real-time.

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
