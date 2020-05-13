import sqlalchemy as sql
import pandas as pd
import os
import sys
import logging
import logging.config
from sqlalchemy import Column, Integer, String, MetaData, create_engine, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config
from helpers import create_connection, get_session
import argparse


logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

logger = logging.getLogger('insurance-db')
Base = declarative_base()

class Insurance(Base):
    """ Defines the data model for the table `insurance`. """

    __tablename__ = 'insurance'

    patient_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    age = Column(Integer, unique=False, nullable=False)
    sex = Column(String(100), unique=False, nullable=False)
    bmi = Column(Float, unique=False, nullable=False)
    smoker = Column(String(100), unique=False, nullable=False)
    region  = Column(String(100), unique=False, nullable=False)
    charges = Column(Float, unique=False, nullable=False)


    def __repr__(self):
        insurance_repr = "<Insurance(patient_id='%i', age='%i', sex='%s', bmi='%f', smoker='%s', region='%s', charges='%f' )>"
        return insurance_repr % (self.patient_id, self.age, self.sex, self.bmi, self.smoker, self.region, self.charges)



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
        return 'sqlite:///insurance.db'



def create_db(args,engine=None):
    """Creates a database with the data models inherited from `Base` (Insurance).
    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.
    Returns:
        None
    """
    if engine is None:
        RDS = eval(args.RDS)
        logger.info("RDS:{}".format(RDS))
        engine = sql.create_engine(get_engine_string(RDS = RDS))

    Base.metadata.create_all(engine)
    logging.info("database created")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default="False",help="True if want to create in RDS else None")
    args = parser.parse_args()
    create_db(args)
