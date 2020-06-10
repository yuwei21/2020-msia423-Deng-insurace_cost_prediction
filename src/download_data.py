import pandas as pd 
import logging
import sys
import os
import boto3
import yaml
import argparse

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

s3_client = boto3.client("s3",
            aws_access_key_id = os.environ.get("aws_access_key_id"),
            aws_secret_access_key= os.environ.get("aws_secret_access_key"))

def download_data (read_path, save_path):
    """Download data from a public S3 bucket to local folder
    Args:
        read_path (str) : path of data source
        save_path (str) ; path to save the data after download
    Returns : None 
    """

    try:
        s3_client.download_file("nw-yuwei-s3", read_path, save_path)
        logger.info("Download file from %s to %s", read_path, save_path)
    except Exception as e:
        logger.error("Unable to download file from public S3 bucket.")
        logger.error(e)
        
def download(args):
    """Run functions defined 
    :param arg: parsed argument input
    :return: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f, yaml.FullLoader)
        download_data(**config['download_data']['download_data'])
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Data from public S3")
    parser.add_argument("--config",default="config/model_config.yaml", help="Path to input to post process")
    args = parser.parse_args()
    download(args)

    
