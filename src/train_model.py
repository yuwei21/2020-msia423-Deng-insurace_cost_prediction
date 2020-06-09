import argparse
import logging
import pandas as pd
import numpy as np
import yaml
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.ensemble import RandomForestRegressor

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def split_data(data, X, y, test_size, seed):
    """Split data for training and testing purposes
    params: 
        X: Input dataframe with features
        y: Input dataframe with target
        test_size: proportion of test data
        seed: seed for random state
    Returns:
         dataframes X_train, X_test, y_train, y_test
    """
    if len(X) != len(data): 
        logger.error("X doesn't have the correct dimension")
        raise ValueError("Length does not match")
    if len(y)!= len(data):
        logger.error("y doesn't have the correct dimension")
        raise ValueError("Length does not match")
    else: 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size , random_state =seed)
        return X_train, X_test, y_train, y_test

def random_forest(X_train, X_test, y_train, y_test, n_estimators, criterion, random_state, n_jobs):
    """Training logistic regression model
    params:
        X_train (:py:class:`pandas.DataFrame`): Training df with features
        X_test (:py:class:`pandas.DataFrame`): Testing df with features
        y_train (:py:class:`pandas.DataFrame`): Training df with target
        y_test (:py:class:`pandas.DataFrame`): Testing df with target
        initial_features: 
    Returns:
        Random Forest Model
    """
    if X_train.empty==True or X_test.empty==True or y_train.empty==True or y_test.empty == True:
        logger.error('Input dataframe is empty')
        raise ValueError("Input dataframe cannot be empty")
    else: 
        rm = RandomForestRegressor(n_estimators = n_estimators, criterion = criterion,random_state = random_state, \
        n_jobs =  n_jobs)
        rm.fit(X_train,y_train.values.ravel())
        return rm


def training(args):
    """Run defined functions
    param arg: parsed argument input
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    data = pd.read_csv(args.input3)
    logger.info('Data loaded from %s', args.input1)
    
    X = pd.read_csv(args.input1)
    logger.info('Features data loaded from %s', args.input1)
    
    y = pd.read_csv(args.input2)
    logger.info('Target data loaded from %s', args.input2)
    X_train, X_test, y_train, y_test = split_data(data,X,y,**config['train_model']['split_data'])
    model = random_forest(X_train, X_test, y_train, y_test,**config['train_model']['random_forest'] )

    with open(args.output1, "wb") as f:
        pickle.dump(model, f)
    logger.info("Trained model object saved to %s", args.output1)
    
    X_train.to_csv(args.output2, index=False)
    logger.info("Training features saved to %s", args.output2)

    y_train.to_csv(args.output3, index=False)
    logger.info("Training target saved to %s", args.output3)

    X_test.to_csv(args.output4, index=False)
    logger.info("Testing features saved to %s", args.output4)

    y_test.to_csv(args.output5, index=False)
    logger.info("Training features saved to %s", args.output5)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Train model")
    parser.add_argument('--input1', default="data/features.csv", help='Path to input data')
    parser.add_argument('--input2', default="data/target.csv", help='Path to input data')
    parser.add_argument('--input3', default="data/insurance.csv", help='Path to input data')
    parser.add_argument('--config', default='config/model_config.yaml',
                        help='path to yaml file with configurations')
    parser.add_argument('--output1', default="models/model.pkl", help='Path to save model(pkl)')
    parser.add_argument('--output2', default="data/train/X_train.csv", help='Path to save output CSV')
    parser.add_argument('--output3', default="data/train/y_train.csv", help='Path to save output CSV')
    parser.add_argument('--output4', default="data/test/X_test.csv", help='Path to save output CSV')
    parser.add_argument('--output5', default="data/test/y_test.csv", help='Path to save output CSV')
    args = parser.parse_args()
    training(args)
