import logging 
import numpy as np
import yaml
import argparse
import pandas as pd


logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def transform_features(data, features_needed):
    """Add additional features, transformation, and interactions into original dataframe.
    Args:
        data (:py:class:`pandas.DataFrame`): Original Dataframe
        features_needed: Features that need to be transformed
  
    Returns:
        data (:py:class:`pandas.DataFrame`): DataFrame containing original and transformed features.
    """
    if set(features_needed).issubset(set(data.columns)) == False:
        logging.error("features are not in main dataset")
        raise ValueError("Required columns not present")
    else:
        data=pd.get_dummies(data, columns=features_needed,drop_first=True)
        return data
            

def choose_features(data,features):
    """choose selected features from dataframe. 
    params:
        data (:py:class:`pandas.DataFrame`): Input DataFrame
        features (:obj:`list`): List of features to extract
    Returns: 
        X (:py:class:`pandas.DataFrame`): DataFrame with selected features
    """
    if set(features).issubset(set(data.columns)) == False:
        logging.error("features are not in main dataset")
        raise ValueError("Required columns not present")
    else:
        X = data[features]
        return X

def get_target(data,target):
    """Choose y label from dataframe.
    params:  
        data (:py:class:`pandas.DataFrame`): Input DataFrame
        target (str) : target label
    Returns: 
        y: (:py:class:`pandas.DataFrame`): DataFrame with target column
    """
    if target not in data.columns:
        logger.error("%s not in main dataset", str(target))
        raise ValueError("Required columns not present")
    else: 
        y = data[target]
        return y
    
def generating(args):
    """Run defined functions
    Args:
        parsed argument input
    Returns:
        None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    df = pd.read_csv(args.input)
    logger.info('Input data loaded from %s', args.input)

    data = transform_features(df,**config['generate_features']['transform_features'])
    data.to_csv(args.output3, index=False)
    logger.info("Processed data saved to %s", args.output3)

    features = choose_features(data, **config['generate_features']['choose_features'])
    y=get_target(data, **config['generate_features']['get_target'])
    
    features.to_csv(args.output1, index=False)
    logger.info("Features saved to %s", args.output1)
  
    pd.DataFrame(y).to_csv(args.output2,index=False)
    logger.info("Target saved to %s", args.output2)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate features.")
    parser.add_argument('--input', default="data/insurance.csv", help='Path to input data')
    parser.add_argument('--config', default='config/model_config.yaml',
                        help='path to yaml file with configurations')
    parser.add_argument('--output1', default="data/features.csv", help='Path to save output CSV')
    parser.add_argument('--output2', default="data/target.csv", help='Path to save output CSV')
    parser.add_argument('--output3', default="data/processed_data.csv", help='Path to save output CSV')
    args = parser.parse_args()

    generating(args)



