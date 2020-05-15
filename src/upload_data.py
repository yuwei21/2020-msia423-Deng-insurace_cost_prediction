import argparse
import boto3
import logging
from botocore.exceptions import ClientError
import os

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
s3_client = boto3.client("s3",aws_access_key_id = os.environ.get("aws_access_key_id"),aws_secret_access_key= os.environ.get("aws_secret_access_key"))

def upload_data(args):
    """upload raw data downloaded in the local folder to an S3 bucket of user input
    Args:
        args (src): parsed argument input -include args.input_file_path, args.bucket_name, args.output_file_path
    
    Returns : None
    """
    try:
        s3_client.upload_file(args.input_file_path,args.bucket_name,args.output_file_path)
        logger.info("Uploaded the file from " + args.input_file_path + " to " + args.bucket_name + " as " + args.output_file_path)
    except boto3.exceptions.S3UploadFailedError as e:
        logger.error(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload data to S3")
    # add argument
    parser.add_argument("--input_file_path", type=str, default = "data/insurance.csv", help="local path for uploaded file")
    parser.add_argument("--bucket_name", help="s3 bucket name")
    parser.add_argument("--output_file_path",type=str, default = "data/insurance.csv", help="output path for uploaded file")

    args = parser.parse_args()
    upload_data(args)
