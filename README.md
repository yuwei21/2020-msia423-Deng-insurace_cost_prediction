# MSiA423 Repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Backlog](#backlog)
- [Directory structure](#directory-structure)

## Project Charter
### Vision
Help people gain a fair idea of the cost of their treatments billed by insurance companies. Help insurance companies determine the appropriate premium they should collect to make profits. 
### Mission
Create an interative web application to predict health care costs given a user's input of factors that may influence the charge of a specific patient. The underlying model will be a regression model based on the Medical Cost Personal Dataset with 1338 observations from Kaggle. This application will assist insurance company in deciding the premiums they should collect to make profits and help people assess their health condition. 
### Success Criteria
- The model will be evaluated by RMSE and R-Squared measures. The sucess of the regression model will be based on achieving an R-Squared above 0.8 on the test dataset. 
- The sucess of the application from the business persective will be measured by the number of visits to app in an interval time and the number of new user engagements throughout the time. 
## Backlog 
## Planning
### Initiative 1
The cost of treatment of each patient depends on many factors: age, type of clinic, city of residence, and so on. The aim of this project is to use these information to obtain an approximation as to what will be the health care costs of the patients and make a conclusion about the health of patients by building regression models. It is also important to go deeply into what factors influence the charge of a specific patient. 
- Epic 1: Create and test models
    - Story 1: Download the data files (Medical Cost Personal Dataset) from Kaggle 
        - Link to data source:[https://www.kaggle.com/mirichoi0218/insurance]
    - Story 2: Perform Early Exploratory Analysis  
        - Conduct data cleaning and EDA
            - Data fromat (Variable structure) 
            - Checking missing values 
            - Feature engineering
    - Story 3: Model Fitting and Selection 
        - Building regression models on randomly selected training data using Linear Regression, Random Forest and Gradient       Boosting 
        - Tune models to optimize performance 
        - Assess and comparing models based on performance metrics (RMSE, R-Squared) on testing data 
    - Story 4: Create Documentation for Models 
    - Epic 2: Exploring additional models 
        - Story 1: Build models like Neural Networks
        - Story 2: Conducting Unsupervised Learning
            - Perform clustering to explore the relationship between charges and predictors
        - Story 3: Create New Features
            - Include interaction terms of features (e.g. obese * smoker, etc.) 
### Initiative 2: Web Application
From the perspective of insurance companies, the insurance company must collect more premiums than the amount paid to the insured person. Thus, the web appplication helps insurance companies have a better understanding of the health costs of their potential customers and set premiums accordingly to make profits. People can also have a fair idea of their health condition and health care costs. The final web application would allow user to input values of the most important factors that affect the charge of patients and return the predicted insurance costs.  
- Epic 1: Brainstrom Core Functionality 
    - Story 1: Create history page, etc. 
- Epic 2: Create App Front End 
    - Story 1: Create web app using HTML, CSS, etc. 
        - Create landing page, etc.
    - Story 2: Improve Web app UI design 
    - Story 3: Test Web Applications 
    - Story 4: Document Web Applications 
- Epic 3: Online Deployment 
    - Story 1: Deploying web app (Flask) on AWS 
    - Story 2: Creating an RDS instance 
    - Story 3: Test web applications 
        - Unit Testing, Configured reproducibility tests, etc.     
- Epic 4: Final Presentation 
    - Story 1: Presentation slides 
        
## Backlog
1. "Initiative1.epic1.story1" (0 pts) - PLANNED
2. "Initiative1.epic1.story2" (4 pts) - PLANNED
3. "Initiative1.epic1.story3"  (8 pts) - PLANNED
4. "Initiative2.epic2.story1" (8 pts) 
5. "Initiative2.epic2.story2" (8 pts)
6. "Initiative2.epic2.story3" (8 pts)
7. "Initiative2.epic3.story1" (8 pts)
8. "Initiative2.epic3.story2" (4 pts)
9. "Initiative2.epic3.story3"  (8 pts)
10. "Initiative2.epic4.story1" (4 pts)

## Icebox
1. "Initiative1.epic1.story1"
2. "Initiative1.epic2.story2"
3. "Initiative1.epic1.story3"
4. "Initiative2.epic1.story1"
5. "Initiative2.epic2.story4"


## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

