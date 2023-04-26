import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
# from cosine import output, filter

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "21Alshow!"
MYSQL_PORT = 3306
MYSQL_DATABASE = "master_database"

mysql_engine = MySQLDatabaseHandler(MYSQL_USER,MYSQL_USER_PASSWORD,MYSQL_PORT,MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded, 
# but if you decide to use SQLAlchemy ORM framework, 
# there's a much better and cleaner way to do this
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get("q")
        query2 = request.form.get("ages")
        query3 = request.form.get("length")
        query4 = request.form.get("player_num")
        return render_template('catalogue.html', tables=(output(query)))
    return render_template('base.html', title="sample html")


app.run(debug=True)