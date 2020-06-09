import pickle
import traceback
import os
import sys
import pandas as pd
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.model import Insurance_Predict


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flaskconfig.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Homepage of this prediction system.
    Returns: rendered html template
    """
    try:
        logger.debug("Index page accessed")
        return render_template('index.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display records, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST', 'GET'])
def add_entry():
    """View that process a POST with new patient input
    Returns: rendered html template with prediction results.
    """
    try:
        global db
        # retrieve features
        age  = request.form['age']
        sex_male = request.form['sex_male']
        bmi = request.form['bmi']
        children = request.form['children']
        smoker_yes = request.form['smoker_yes']
        region_southwest = request.form['region_southwest']
        region_northwest = request.form['region_northwest']
        region_southeast  = request.form['region_southeast']
        logger.info("all inputs retrieved!")

        # load trained model
        model_path = app.config["MODEL_PATH"]
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        logger.info("model loaded.")

        # create a dataframe to store inputs for prediction
        insurance_df = pd.DataFrame(columns=["age", "sex_male", "bmi", "children",
                                        "smoker_yes", "region_southwest", "region_northwest",
                                        "region_southeast"])

        insurance_df.loc[0] = [age, sex_male, bmi, children, smoker_yes, region_southwest,
                               region_northwest, region_southeast]


        # change datatype from object to float
        insurance_df = insurance_df.astype("float")
        # Make a prediction
        cost_pred = model.predict(insurance_df)
        pred =  cost_pred[0]

        logger.info("prediction made: {:0.3f}".format(pred))

        customer1 = Insurance_Predict (age=float(age),
                              sex_male=float(sex_male),
                              bmi=float(bmi),
                              children=float(children),
                              smoker_yes=float(smoker_yes),
                              region_southwest=float(region_southwest),
                              region_northwest=float(region_northwest),
                              region_southeast=float(region_southeast),
                              predicted_charge=float(pred))

        db.session.add(customer1)
        db.session.commit()
        logger.info("Data added.")
        query_result = db.session.query(Insurance_Predict).all()
        logger.info(query_result)

        result = "You will spend ${:.2f} on treatments.".format(pred)
        return render_template('index.html', result=result)
    except:
        traceback.print_exc()
        logger.warning("Not able to display evaluations, error page returned")
        return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])