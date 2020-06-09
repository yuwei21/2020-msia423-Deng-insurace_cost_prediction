import sqlalchemy as sql
import pandas as pd
import os
import sys
import logging
from sqlalchemy import Column, Integer, String, MetaData, create_engine, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import argparse


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger('insurance-db')
Base = declarative_base()

class Insurance_Predict(Base):
    """ Defines the data model for the table `insurance`. """

    __tablename__ = 'insurance_predict'

    patient_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    age = Column(Integer, unique=False, nullable=False)
    sex_male = Column(Integer, unique=False, nullable=False)
    bmi = Column(Float, unique=False, nullable=False)
    children = Column(Integer, unique=False, nullable=False)
    smoker_yes = Column(Integer, unique=False, nullable=False)
    region_southwest = Column(Integer, unique=False, nullable=False)
    region_northwest = Column(Integer, unique=False, nullable=False)
    region_southeast = Column(Integer, unique=False, nullable=False)

    predicted_charge = Column(Float, unique=False, nullable=False)


    def __repr__(self):
        insurance_repr = "<Insurance_Predict(patient_id='%i', age='%i', sex_male='%i', bmi='%f', children='%i', smoker_yes='%i', region_southwest='%i', \
        region_northwest='%i', region_southeast='%i', predicted_charge='%f')>"
        return insurance_repr % (self.patient_id, self.age, self.sex_male, self.bmi, self.children, self.smoker_yes, self.region_southwest, \
            self. region_northwest, self.region_southeast, self.predicted_charge)



def get_engine_string(conn_type = "mysql+pymysql"):
    """ Get database engine path. 
    Args:
        conn_tyep (str): Name of sql connection.
    Returns:
        engine_string (str): String defining SQLAlchemy connection URI.
    """

    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    
    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(conn_type, user, password, host, port, DATABASE_NAME)
    logging.debug("engine string:{}".format(engine_string))
    return  engine_string


def create_db(args):
    """Creates a database with the data models inherited from `Base` (Insurance).
    Args:
        RDS: True if create database in RDS otherwise None
    Returns:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
    """
    if args.RDS:
        engine_string=get_engine_string()
    else:
        engine_string = args.local_URI
    logger.info("RDS:%s" % args.RDS)
    engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logging.info("database created successfully")

    return engine


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default=False,help="True if create in RDS otherwise None")
    parser.add_argument("--local_URI", default='sqlite:///data/Insurance_Predict.db')
    args = parser.parse_args()
    
    engine = create_db(args)

    Session = sessionmaker(bind=engine)  
    session = Session()
    # add precalculated users and charges
    first_user = Insurance_Predict(age=35,sex_male=1,bmi=36.67,children=1,
        smoker_yes=1,region_southeast=0,region_northwest=0, region_southwest=0,predicted_charge=40767.124596199974)
    session.add(first_user)
    session.commit()

    logger.info("Data added")

    query = "SELECT * FROM insurance_predict"
    df = pd.read_sql(query, con=engine)
    logger.info(df)
    session.close()

