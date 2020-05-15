import sqlalchemy as sql
import pandas as pd
import os
import sys
import logging
from sqlalchemy import Column, Integer, String, MetaData, create_engine, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from helpers import create_connection, get_session
import argparse
import config

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger('insurance-db')
Base = declarative_base()

class Insurance_Predict(Base):
    """ Defines the data model for the table `insurance`. """

    __tablename__ = 'insurance_predict'

    patient_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    age = Column(Integer, unique=False, nullable=False)
    sex = Column(String(100), unique=False, nullable=False)
    bmi = Column(Float, unique=False, nullable=False)
    smoker = Column(String(100), unique=False, nullable=False)
    region  = Column(String(100), unique=False, nullable=False)
    charges = Column(Float, unique=False, nullable=False)

    predicted_charge = Column(Float, unique=False, nullable=False)


    def __repr__(self):
        insurance_repr = "<Insurance_Predict(patient_id='%i', age='%i', sex='%s', bmi='%f', smoker='%s', region='%s', charges='%f', predicted_charge='%f' )>"
        return insurance_repr % (self.patient_id, self.age, self.sex, self.bmi, self.smoker, self.region, self.charges,self.predicted_charge)



def get_engine_string(RDS = False):
    """ Get database engine path. """
    if RDS:
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        DATABASE_NAME = 'msia423_db'
        engine_string = "{}://{}:{}@{}:{}/{}". \
            format(conn_type, user, password, host, port, DATABASE_NAME)
        # print(engine_string)
        logging.debug("engine string:{}".format(engine_string))
        return  engine_string
    else:
        return config.SQLALCHEMY_DATABASE_URI



def create_db(args,engine=None):
    """Creates a database with the data models inherited from `Base` (Insurance).
    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
    Returns:
        None
    """
    if engine is None:
        RDS = eval(args.RDS)
        logger.info("RDS:%s",RDS)
        engine = sql.create_engine(get_engine_string(RDS = RDS))

    Base.metadata.create_all(engine)
    logging.info("database created")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default="False",help="True if create in RDS otherwise None")
    args = parser.parse_args()
    create_db(args)

