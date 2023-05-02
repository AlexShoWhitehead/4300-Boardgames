import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from cosine import output

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = ""
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
def sql_search(age, length, players):
    query_sql = f"""SELECT * FROM boardgames"""
    if (age != '' and length == '' and players == ''):
        query_sql = f"""SELECT * FROM boardgames WHERE (min_age <= {age})""" 
    elif (age != '' and length != '' and players == ''):
        query_sql = f"""SELECT * FROM boardgames WHERE (min_age <= {age}) 
            AND (play_time <= {length})"""
    elif (length != '' and age == '' and players == ''):
        query_sql = f"""SELECT * FROM boardgames WHERE (play_time <= {length})"""
    elif (length != '' and players != '' and age == ''):
        query_sql = f"""SELECT * FROM boardgames WHERE )
            (play_time <= {length})
            AND (min_players <= {players})
            AND (max_players >= {players})"""
    elif (age != '' and length == '' and players != ''):
        query_sql = f"""SELECT * FROM boardgames WHERE (min_age <= {age})
            AND (min_players <= {players})
            AND (max_players >= {players})"""
    elif (length == '' and players != '' and age == ''):
         query_sql = f"""SELECT * FROM boardgames WHERE (min_players <= {players})
            AND (max_players >= {players})"""
    elif (age != '' and length != '' and players != ''):
        query_sql = f"""SELECT * FROM boardgames WHERE (min_age <= {age})
            AND (play_time <= {length})
            AND (min_players <= {players})
            AND (max_players >= {players})"""
    keys = ["id","name", "year_published", "min_players", "max_players", "play_time",
            "min_age", "users_rated", "rating_average", "bgg_rank", "complexity_average",
            "owned_users", "mechanics", "domains", "categories", "statistical_data",
            "qualitative_data", "image_data", "users_commented", "comments"] 
    data = mysql_engine.query_selector(query_sql)
    return json.dumps([dict(zip(keys,i)) for i in data])

query = ''
query2 = ''
query3 = ''
query4 = ''

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get("q")
        secondQuery = request.form.get("relevant")
        query2 = request.form.get("ages")
        query3 = request.form.get("length")
        query4 = request.form.get("player_num")
        sum = request.form.get("tunnel")
        if secondQuery != None:
            return render_template('catalogue.html', tables = (sum))
        else:
            return render_template('twostep.html', tables=(output(query, sql_search(query2, query3, query4))))
    return render_template('base.html', title="sample html")


app.run(debug=True)