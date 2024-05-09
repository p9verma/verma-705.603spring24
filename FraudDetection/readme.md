# Fraud Detection - Case study
## Module 5

*Author: Punita Verma*

**Contents**
* Analysis directory: This directory contains the module necessary for data analysis. One of the goals of this case study is to implement best practices of module code development. This is demonstrated in the modules contained in this directory for all steps of the prediction pipeline from input to output.
* Results directory: This directory contains results from the model trainings. The results are generated using the metrics module and contain useful information that can be used to understand model performance, strengths, and weaknesses. This is an important aspect of the AI system post deployment as monitoring and updating the model require a thorough quantitative assesment of the existing model performance.
* ML microservice: [Deliverable_G.ipynb](analysis/Deliverable_G.ipynb) and [Deliverable_G_run.ipynb](Deliverable_G_run.ipynb) contain the code demonstrating how to run the ml microservice (via flask app) defined in [ml_microservice.py](analysis/ml_microserivce.py). The ETL pipeline, dataset pipeline, and model pipeline all all run as part of the (model.py)[analysis/model.py) and ml_microservice.py.

*Note:* I am experiencing issues getting Docker image to identify my custom python modules (i.e. Metrics.py, ETL_pipeline.py etc.) that are placed in different working directories (as per assignment specifications). I spent a significant amount of time fixing this but was unable to get the import statements to run. Docker image may have some issues. 
