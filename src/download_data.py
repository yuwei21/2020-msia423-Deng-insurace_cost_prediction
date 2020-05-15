import pandas as pd 
import logging
import sys
import os

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def download_data (read_path, save_path):
    """Download data from a public S3 bucket to local folder
    Args:
        read_path (str) : path of data source
        save_path (str) ; path to save the data after download
    Returns : None 
    """

    try:
        df = pd.read_csv(read_path, sep=",")
        df.to_csv(save_path)
        logger.info("Download file from %s to %s", read_path, save_path)
    except Exception as e:
        logger.error(e)
        
if __name__ == "__main__":
    url = "https://s3-public-nw.s3.us-east-2.amazonaws.com/insurance-source/insurance.csv"
    download_data(url,"data/insurance.csv")
    
