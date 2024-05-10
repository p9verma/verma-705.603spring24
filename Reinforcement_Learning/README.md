# Reinforcement (Q-learning) - Email Case study
## Module 14

*Author: Punita Verma*

**Contents**
* Analysis directory: This directory contains the module necessary for data analysis. One of the goals of this case study is to implement best practices of module code development. This is demonstrated in the modules contained in this directory for all steps of the prediction pipeline from input to output.
* Results directory: This directory contains results from the model trainings. The results are generated using the metrics module and contain useful information that can be used to understand model performance, strengths, and weaknesses. This is an important aspect of the AI system post deployment as monitoring and updating the model require a thorough quantitative assesment of the existing model performance.
* To see a demonstration on how the pipelines (ETL Pipeline, model pipeline, and metrics pipeline) are run, see [Assignment10RL.ipynb](Assignment10RL.ipynb). This notebook also contains exploratory data analysis and model performance details.
* ML microservice: The ml microservice (flask app) defined in [ml_microservice.py](analysis/ml_microserivce.py), runs on a docker image created using the Dockerfile and requirements.txt. This app encapsulate the model's predict() method in order to output an action (subject line id).
