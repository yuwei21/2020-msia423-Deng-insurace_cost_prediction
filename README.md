# MSiA423 Repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Backlog](#backlog)
- [Data Sources](#data-sources)

## Project Charter
### Vision
Help people gain a fair idea of the cost of their treatments billed by insurance companies. Help insurance companies determined the appropriate premium they should collect to make profits. 
### Mission
Create an interative web application to predict health care costs given a user's input of factors that may influence the charge of a specific patient. The underlying model will be a regression model based on the Medical Cost Personal Dataset with 1338 observations from Kaggle. This application will assist insurance company in deciding the premiums they should collect to make profits.
### Success Criteria
- The model will be evaluated by RMSE and R-Squared measures. The sucess of the regression model will be based on achieving an R-Squared above 0.8 on the test dataset. 
- The sucess of the application from the business persective will be measured by the number of visits to app in an interval time and the number of new user engagements throughout the time. 
## Backlog 
### Initiatives
The cost of treatment of each patient depends on many factors: age, type of clinic, city of residence, and so on. The aim of this project is to use these information to obtain an approximation as to what will be the health care costs of the patients and make a conclusion about the health of patients. It is also important to go deeply into what factors influence the charge of a specific patient. Besides, from the perspective of insurance companies, the insurance company must collect more premiums than the amount paid to the insured person. Thus, the predictive model also helps insurance companies to have a better understanding of the health costs of their potential customers and set premiums accordingly to make profits. The final web application would allow user to input values of the most important factors that affect the charge of patients and return the predicted insurance costs.  
### Epics
**Epic 1: Data Preparation** 
- Story #1: Downloading the data files (red wine & white wine) from UCI Machine Learning Repository (1 pt) **(Planned for the next 2 weeks)**
    - **Backlog**
    - Link to data source:[https://archive.ics.uci.edu/ml/datasets/wine+quality]
- Story #2: EDA and Data Cleaning (2 pts) **(Planned for the next 2 weeks)**
    - **Backlog**
    - Conducting exploratory data analysis (variable structures, distribution of variables, etc.)
    - Performing data cleaning (null values, outliers, etc.)
    
**Epic 2: Modeling and Model Selection** 
- Story #1: Building classification models on randomly selected training data using Random Forest, XGBoost, and Neural Networks (4 pts) **(Planned for the next 2 weeks)**
    - **Backlog**
- Story #2: Comparing models based on performance metrics (Accuracy) on testing data (2 pts) **(Planned for the next 2 weeks)**
    - **Backlog**
- Story #3: Exploring additional models (e.g. CNN, SVM)
    -   **Icebox**
- Story #4: Reviewing models with QA partner (4 pts)
    - **Backlog**
    
**Epic 3: Online Deployment and Testing** 
- Story #1: Web app UI design (8 pts)
    - **Backlog**
- Story #2: Deploying web app (Flask) on AWS (8 pts)
    - **Backlog**
- Story #3: Creating an RDS instance (4 pts)
    - **Backlog**
- Story #4: Testing (Unit tests and Configured reproducibility tests) (8 pts)
    - **Backlog**
    
**Epic 4: Final Presentation**  
- Story #1: Presentation slides (4 pts)
    - **Backlog**


## Data Sources


