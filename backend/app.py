import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from new_cosine import output
import csv
import pandas as pd

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

def make_dataframe(csv_path, delimiter):
    rows = []
    with open(csv_path, newline='', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_ALL)
        for row in reader:
            for col in range(len(row)):
                row[col].replace("â€™", "'")
            rows.append(row)
        csvfile.close()

    df = pd.DataFrame(rows)
    df.columns = df.iloc[0]
    df = df[1:]

    return df

# Sample search, the LIKE operator in this case is hard-coded, 
# but if you decide to use SQLAlchemy ORM framework, 
# there's a much better and cleaner way to do this
def sql_search(age, length, players):
    game_data = make_dataframe('datasets/master_database.csv', ';')
    print(age, length, players)
    if(age != ''):
        game_data = game_data[game_data['min_age'].astype('int') <= int(age)]
    if(length != ''):
        game_data = game_data[game_data['play_time'].astype('int') <= int(length)]
    if(players != ''):
        game_data = game_data[game_data['min_players'].astype('int') <= int(players)]
        game_data = game_data[game_data['max_players'].astype('int') >= int(players)]
    return game_data

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