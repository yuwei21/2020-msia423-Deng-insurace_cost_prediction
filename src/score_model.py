import argparse
import logging
import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.ensemble import RandomForestRegressor

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def score_model(rm, X_train, X_test):
    """ Score testing data using generated model
    params:
        rm: model 
        X_train (:py:class:`pandas.DataFrame`): train dataframe with features
        X_test (:py:class:`pandas.DataFrame`): testing dataframe with features
        
    Returns: 
        train_pred (array): 
        test_pred (array): class prediction  
    """
    if str(type(rm)) != "<class 'sklearn.ensemble.forest.RandomForestRegressor'>":
        logger.error("model incorrect.")
        raise TypeError("model used to score must be Random Forest Regression.")
    if (rm.get_params()) != {'bootstrap': True, 'criterion': 'mse', 'max_depth': None, \
        'max_features': 'auto', 'max_leaf_nodes': None, 'min_impurity_decrease': 0.0, 'min_impurity_split': None, \
            'min_samples_leaf': 1, 'min_samples_split': 2, 'min_weight_fraction_leaf': 0.0, 'n_estimators': 100, 'n_jobs': -1, \
                'oob_score': False, 'random_state': 1, 'verbose': 0, 'warm_start': False}:
        logger.error("Model is incorrect")
        raise ValueError("The Model is incorrect")

    else: 
        train_pred = rm.predict(X_train)
        test_pred = rm.predict(X_test)
        return train_pred, test_pred 
        

def scoring(args):
    """Run defined functions
    Args:
        parsed argument input
    Returns:
        None
    """
    with open(args.input1, "rb") as f:
        rm = pickle.load(f)
    logger.info("Trained model object retrieved from %s", args.input1)

    X_test = pd.read_csv(args.input2)
    logger.info('X_test loaded from %s', args.input2)

    X_train = pd.read_csv(args.input3)
    logger.info('X_train loaded from %s', args.input3)

    train_pred, test_pred = score_model(rm, X_train, X_test)
    
    pd.DataFrame(train_pred).to_csv(args.output1, index=False)
    logger.info("Train prediction saved to %s", args.output1)

    pd.DataFrame(test_pred).to_csv(args.output2, index = False)
    logger.info("Test prediction saved to %s", args.output2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score model.")
    parser.add_argument('--input1', default="models/model.pkl", help='Path to retreive trained model')
    parser.add_argument('--input2', default="data/test/X_test.csv", help='Path to retreive test features')
    parser.add_argument('--input3', default="data/train/X_train.csv", help='Path to retreive test features')
    parser.add_argument('--output1', default="data/train/train_prediction.csv", help='Path to save output CSV')
    parser.add_argument('--output2', default="data/test/test_prediction.csv", help='Path to save output CSV')
    args = parser.parse_args()

    scoring(args)

