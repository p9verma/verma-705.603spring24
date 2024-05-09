# Automated License Plate Recognition Project- Case study
## Module 8

*Author: Punita Verma*

**Contents**
* Analysis directory: This directory contains the module necessary for data analysis. One of the goals of this case study is to implement best practices of module code development. This is demonstrated in the modules contained in this directory for all steps of the prediction pipeline from input to output.
* Results directory: This directory contains results from the model trainings. The results are generated using the metrics module and contain useful information that can be used to understand model performance, strengths, and weaknesses. This is an important aspect of the AI system post deployment as monitoring and updating the model require a thorough quantitative assesment of the existing model performance.
* Dockerized System Architecture: [udp.py](udp.py), [Dockerfile](Dockerfile), and [requirements.txt](requirements.txt) contain the code to livestream a video via ffmpeg using RTSP/UDP video streaming. The streamed video can be used in sync to feed the model.py and create predictions.
