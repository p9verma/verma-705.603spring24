# MOTIVATION (Why's)
## **Why are we solving this problem?**

### <u>Problem Statement</u>

Amazon has identified a need to move beyond the traditional 5-star rating system. This system inherently includes limitations and subjectivity.The company aims to develop a more nuanced and reliable method of capturing customer feedback and product quality. 

### <u>Value Proposition</u>

The benefits of creating a system to move beyond the traditional 5-star rating system will allow Amazon to facilitate more meaningful insights when reviewing purchases and consuming reviews and better feeback for businesses selling reviewed products. 

## **Why is our solution a viable one?**

An ML solution fits this problem because the traditional 5-star rating system is limited in it's ability to scale further than a quantitative score. To encode greater, more meaningful information in a review label, we must consider an ML solution. Patterns in the data that indicate reviewer sentiment may be detected by humans but it is not feasible in large quantities such as all Amazon reviews.may be convoluted in complex mathematical regression or correlation amongst multiple factors or features.The ML solution will provide the quantitative robustness and automation needed in this system. We can tolerate a reasonable degree of mistakes in this system, as ultimately, most incorrectly classified reviews are not life-threatening. 
 
# REQUIREMENTS (What's)
## **SCOPE:**

### <u>What are our goals?</u>

One of the main goals of this system is to mark reviews based on their overall sentiment. The model should consider a probability computed from the training-based predictions that will guide the system’s label for the transaction. This is a systematic goal that will help the user understand wholistically the reviewer's intentions. The overall system will require the user to ultimately use some contextual and human inputs to determine the actual sentiment of the review. The goal of the model is to guide in this decision making process.
 
### <u>What are the success criteria?</u>

The success criteria in this system will be tests performed on labeled data. Since the system will perform predictions in an unsupervised environment, it is difficult to get error scores in the real world. We can do the best my finetuning the model before deployment. However, in the input data we have the quantitative 5-star rating. This can be encoded to extract what the reviewer *intends* for the review sentiment to be and succes metrics can be basedvon this "ground truth". Some metrics we can use to evaluate the runtime performance of the system are precision, recall, and F1-score. These metrics go beyond accuracy to measure the performance of a model.
 
## **REQUIREMENTS:**

### <u>What are our (system) Assumptions?</u>
- The input data is textual.
- There are underlying patterns that can be detected from review text to aid the development of a usable ML model.
- The data inputted in this system is not highly sensitive as reviews are public. 
 
### <u>What are our (system) Requirements?</u>
- Input review data is in a csv format with text and rating features.
- The system must have a reasonably large memory and gpu/cpu operating capability to process complex prediction methods on large datasets.
- The Natural Language Tookit is available for downloading dependencies.
 
## **RISK & UNCERTAINTIES:**

### <u>What are the possible harms?, What are the causes of mistakes</u>

The possible harms in this system can be emotional and financial damage. If a review is incorectly labelled by the model, the user may lose trust in Amazon's review system and the business/movie being reviewed may incur reputational damage. 
Some cases of errors or mistakes include the manner in which data is created for the model. Inconsistencies or discrepancies in the reviewer's rating score (used for metrics) from what is actually true will skew the model, as it is developed based on the reviewer's own rating. This is a drawback in our system. Future work may involve creating a more robust ground truth based on other features. This may involve a unique/normalized rating scale for each user that scales standard 5-star ratings based on the user's history of ratings, average rating feature, review title feature's extracted sentiment and helpful vote feature.
 
# IMPLEMENTATION (How's)
## **DEVELOPMENT:**
### <u>Methodology</u>
The ETL_Pipeline class is defined in **[data_pipeline](./data_pipeline.py)**. This class contains three main functional methods supporting ETL processing: extract(), transform(), and load().

Extract(): This function takes in a parameter called *filename* indicating the .csv file carrying data and extracts into a dataframe. This function returns the dataframe.

Transform(): This function accepts a dataframe and input and processes it to create new features. These features are extracted based on findings from data analysis performed in **[exploratory_data_analysis.ipynb](analysis/exploratory_data_analysis.ipynb)**. For sentiment analysis, we require cleaning up the data frame and using the feature 'rating', 'review_title', 'text', 'helpful_vote', 'average_rating'.

This function contains all the processes needed to clean, process, and prepare the data for modeling.

Load(): This function accepts a dataframe and saves it to a csv file titled *reviews_processed.csv*

The Reviews_Dataset class defined in **[dataset.py](./dataset.py)** takes in a datafram upon instantiation and splits it into a training, testing and validation set using an 80%, 10%, 10% split respectively. The splits are accesible via helper methods in the class: *get_training_dataset()*, *get_testing_dataset()*, and *get_validation_dataset()*.

The Metrics class defined in **[metrics.py](metrics.py)** generates a report and outputs metrics for model evaluation given a set of prediction and truth values. 


### <u>High-level System Design</u>

At a high level, this system stores data in a csv format, processes and predict review sentiment. We use the Valence Aware Dictionary and sEntiment Reasoner ([VADER](https://github.com/cjhutto/vaderSentiment)) model. This "is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media, and works well on texts from other domains." (https://github.com/cjhutto/vaderSentiment). It was chosen for this task due to the nature of most reviews being brief and informal, similar to social media text which VADER excels in analysing. A *compound* score is used to label reviews as 'negative', 'neutral', or 'positive'.

From VADER github:
> The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence. Calling it a 'normalized, weighted composite score' is accurate.


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
