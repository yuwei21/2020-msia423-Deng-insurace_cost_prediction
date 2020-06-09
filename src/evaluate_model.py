import argparse
import logging
import pandas as pd
import numpy as np
import yaml
import pickle
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.ensemble import RandomForestRegressor

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def evaluate_models(y_train, y_test, train_pred, test_pred):
    """Evaluate the performance of model
    params:
        y_train (:py:class:`pandas.DataFrame`): Testing df with train target
        y_test (:py:class:`pandas.DataFrame`): Testing df with test target
        train_pred (array): train prediction
        test_pred (array): test prediction 
    """
    if y_train.empty == True or y_test.empty==True or train_pred.empty == True or test_pred.empty==True:
        logger.error("Input dataframe(s) is/are empty")
        raise ValueError("Input dataframe cannot be empty")
    MSE_train = mean_squared_error(y_train,train_pred)
    r2_train = r2_score(y_train,train_pred)
    MSE_test = mean_squared_error(y_test,test_pred)
    r2_test = r2_score(y_test,test_pred)
    return MSE_train, r2_train, MSE_test, r2_test

def feature_importance (rm, X, save_fig):
    """ Make a bar plot to show the features importances"""
    feature_importance = rm.feature_importances_
    # make importances relative to max importance
    feature_importance = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)[:20]
    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    plt.yticks(pos, X.columns[sorted_idx])
    plt.xlabel('Relative Importance')
    plt.title('Variable Importance')
    plt.show()
    plt.savefig(save_fig)

def evaluating(args):
    """Run defined functions
    Args:
        parsed argument input
    Returns:
        None
    """  
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    y_test = pd.read_csv(args.input1)
    logger.info('y_test loaded from %s', args.input1)

    y_train = pd.read_csv(args.input2)
    logger.info('y_train loaded from %s', args.input2)

    train_pred = pd.read_csv(args.input3)
    logger.info('Train prediction loaded from %s', args.input3)

    test_pred = pd.read_csv(args.input4)
    logger.info('Test prediction loaded from %s', args.input4)
    MSE_train, r2_train, MSE_test, r2_test = evaluate_models(y_train, y_test, train_pred, test_pred)


    X = pd.read_csv(args.input5)
    logger.info('Features loaded from %s', args.input5)
    
    with open(args.input6, "rb") as f:
        rm = pickle.load(f)
    logger.info("Trained model object retrieved from %s", args.input6)

    feature_importance (rm, X, **config['evaluate_model']['feature_importance'])



    with open(args.output, 'w') as f:
        f.write('MSE train data: %.3f, MSE test data: %.3f' % (MSE_train,MSE_test) + "\n")
        f.write('R2 train data: %.3f, R2 test data: %.3f' % (r2_train, r2_test))
        f.close()

    logger.info("Model performance measures saved to %s", args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate model.")
    parser.add_argument('--input1', default="data/test/y_test.csv", help='Path to retreive test target')
    parser.add_argument('--input2', default="data/train/y_train.csv", help='Path to retreive test target')
    parser.add_argument('--input3', default="data/train/train_prediction.csv", help='Path to retreive probability prediction')
    parser.add_argument('--input4', default="data/test/test_prediction.csv", help='Path to retreive class prediction')
    parser.add_argument('--input5', default="data/features.csv", help='Path to retreive features dataset')
    parser.add_argument('--input6', default="models/model.pkl", help='Path to retreive trained model')
    parser.add_argument('--config', default='config/model_config.yaml',
                        help='path to yaml file with configurations')
    parser.add_argument('--output', default="models/model_performance.txt", help='Path to save output txt')
    args = parser.parse_args()

    evaluating(args)



