import sys
import os
import logging 
import numpy as np
import argparse
import pandas as pd
import pytest
import yaml
from pandas.util.testing import assert_frame_equal
from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.ensemble import RandomForestRegressor

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.generate_features import *
from src.train_model import *
from src.evaluate_model import *
from src.score_model import *

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s',level=logging.INFO)
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def test_transform_features():
    data = pd.read_csv("data/insurance.csv")

    features_needed = ['sex', 'smoker','region']

    features_needed_bad = ['sex','smoker','company']

    ## Happy Path
    output = pd.get_dummies(data, columns=features_needed, drop_first=True)
    assert_frame_equal(output, transform_features(data, features_needed))

    # Unhappy Path
    with pytest.raises(Exception) as excinfo:
        transform_features(data, features_needed_bad)
    assert str(excinfo.value) == "Required columns not present"

def test_choose_features():
    data = pd.read_csv("data/processed_data.csv")
    features = ['age', 'sex_male', 'bmi', 'children','smoker_yes', \
                'region_southwest', 'region_northwest', 'region_southeast']
    
    features_bad = ['age', 'sex_female', 'bmi', 'children','smoker_yes', \
                'region_southwest', 'region_northwest', 'region_southeast']
    # Happy path
    output = data[features]
    assert_frame_equal(output, choose_features(data,features))

    #Unhappy path
    with pytest.raises(Exception) as excinfo:
        choose_features(data,features_bad)
    assert str(excinfo.value) == "Required columns not present"

def test_get_target():
    data = pd.read_csv("data/processed_data.csv")
    target = "charges"
    target_bad = "charge"
    
    # Happy path
    output = pd.DataFrame(data[target])
    assert_frame_equal(output, pd.DataFrame(get_target(data,target)))

    #Unhappy path
    with pytest.raises(Exception) as excinfo:
        get_target(data,target_bad)
    assert str(excinfo.value) == "Required columns not present"

def test_split_data():
    data = pd.read_csv("data/processed_data.csv")
    X = data.drop('charges',axis=1)
    y = data['charges']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2 , random_state =15)
    X_train_df, X_test_df, y_train_df, y_test_df = split_data(data, X, y, 0.2, 15)
    
    # Happy Path
    assert_frame_equal(X_train, X_train_df)
    assert_frame_equal(X_test,X_test_df)
    assert_frame_equal(pd.DataFrame(y_train), pd.DataFrame(y_train_df))
    assert_frame_equal(pd.DataFrame(y_test), pd.DataFrame(y_test_df))

    # Unhappy Path
    X_bad = X.head(10)
    with pytest.raises(Exception) as excinfo:
        split_data(data, X_bad, y, 0.2, 15)
    assert str(excinfo.value) == "Length does not match"


def test_random_forest():
    data = pd.read_csv("data/processed_data.csv")
    X = data.drop('charges',axis=1)
    y = data['charges']
    # Happy path
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2 , random_state =15)
    rm = random_forest(X_train, X_test, y_train, y_test, 100, "mse" , 1, -1)
    rm.fit(X_train,y_train.values.ravel())
    # Check model type
    assert str(type(rm)) == "<class 'sklearn.ensemble.forest.RandomForestRegressor'>"
    
    # Unhappy path
    X_train_bad = pd.DataFrame()
    with pytest.raises(Exception) as excinfo:
        random_forest(X_train_bad, X_test, y_train, y_test, 100, "mse" , 1, -1)
    assert str(excinfo.value) == "Input dataframe cannot be empty"
    

def test_score_model():
    data = pd.read_csv("data/processed_data.csv")
    X = data.drop('charges',axis=1)
    y = data['charges']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2 , random_state =15)
    
    # Happy Path
    rm = RandomForestRegressor(n_estimators = 100, criterion = 'mse',random_state = 1, \
        n_jobs =  -1)
    rm.fit(X_train,y_train.values.ravel())
    train_pred = rm.predict(X_train)
    test_pred = rm.predict(X_test)
    train_pred_df, test_pred_df = score_model(rm, X_train, X_test)
    assert_frame_equal(pd.DataFrame(train_pred), pd.DataFrame(train_pred_df))
    assert_frame_equal(pd.DataFrame(test_pred),pd.DataFrame(test_pred_df))

    ## Unhappy Path
    rm_b = RandomForestRegressor(n_estimators = 100, criterion = 'mse',random_state = 5, \
        n_jobs =  -1)
    rm_b.fit(X_train,y_train.values.ravel())
    with pytest.raises(Exception) as excinfo:
        score_model(rm_b, X_train, X_test)
    assert str(excinfo.value) == "The Model is incorrect"
 
def test_evaluate_model():
    data = pd.read_csv("data/processed_data.csv")
    X = data.drop('charges',axis=1)
    y = data['charges']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2 , random_state =15)
    rm = RandomForestRegressor(n_estimators = 100, criterion = 'mse',random_state = 1, \
        n_jobs =  -1)
    rm.fit(X_train,y_train.values.ravel())
    train_pred = pd.DataFrame(rm.predict(X_train))
    test_pred = pd.DataFrame(rm.predict(X_test))
    MSE_train = mean_squared_error(y_train,train_pred)
    r2_train = r2_score(y_train,train_pred)
    MSE_test = mean_squared_error(y_test,test_pred)
    r2_test = r2_score(y_test,test_pred)
    MSE_train1, r2_train1, MSE_test1, r2_test1 = evaluate_models(y_train, y_test, train_pred, test_pred)
    ## Happy path
    assert MSE_train == MSE_train1
    assert r2_train == r2_train1
    assert  MSE_test == MSE_test1
    assert r2_test == r2_test1

    ## Unhappy path
    y_train_bad = pd.DataFrame()
    with pytest.raises(Exception) as excinfo:
        evaluate_models(y_train_bad, y_test, train_pred, test_pred)
    assert str(excinfo.value) == "Input dataframe cannot be empty"


if __name__ == "__main__":
    test_transform_features()
    test_choose_features()
    test_get_target()
    test_split_data()
    test_random_forest()
    test_score_model()
    test_evaluate_model()
    logger.info("All unit tests completed!")





    
    

