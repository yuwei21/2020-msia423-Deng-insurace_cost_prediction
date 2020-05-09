import pandas as pd
import logging

logger = logging.getLogger(__name__)


def data_download(read_path,save_path):
	"""Download data from a public S3 to specified path
	Args:
		read_path (str): path to data source
		save_path (str): save path of data
	"""
    df = pd.read_csv(url,sep=';')
    df.to_csv(save_path)


if __name__ == "__main__":
    url = 'https://nw-yuwei-s3.s3.us-east-2.amazonaws.com/insurance.csv'
    data_download(url,'data/insurance.csv')