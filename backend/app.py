import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from new_cosine import output, build_inverted_index, tokenize
import csv
import pandas as pd
import ast
from preprocessing import pre_inv, read_mat
import numpy as np

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

def make_matrix(query, results):
  sim_scores = np.empty(len(results))
  for i in range(len(results)):
    sim_scores[i] = results[i]
  return sim_scores

def rocchio(summation, relevant, irrelevant,a=1, b=.3, c=.7, clip = True):
    for element in summation:
        initQuery = a * float(element[1])
        if not len(relevant) == 0:
            secondPre = b * (1 / len(relevant))
            secondSum = int(relevant[0][1])
            for d in range(len(relevant) - 1):
                print(relevant[d + 1][1])
                secondSum = secondSum + int(relevant[d + 1][1])
            secondSum = secondPre * float(secondSum)
            initQuery = initQuery + secondSum
        if not len(irrelevant) == 0:
            thirdPre = c * (1 / len(irrelevant))
            thirdSum = int(irrelevant[0][1])
            for i in range(len(irrelevant) - 1):
                thirdSum = thirdSum + int(irrelevant[i + 1][1])
            thirdSum = thirdPre * float(thirdSum)
            initQuery = initQuery - thirdSum
        element[1] = str(int(initQuery))
    return sorted(summation, key=lambda x: int(x[1]), reverse=True)

# pre_inv(build_inverted_index, make_dataframe, tokenize)
invind = read_mat('datasets/inv_ind.txt')
idf = read_mat('datasets/idf.txt')

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get("q")
        secondQuery = request.form.get("relevant")
        query2 = request.form.get("ages")
        query3 = request.form.get("length")
        query4 = request.form.get("player_num")
        homeQuery = request.form.get("gohome")
        details = request.form.get("details")
        detailsInfo = request.form.get("detailpage")
        if(details != None):
            detailsInfo = ast.literal_eval(detailsInfo)
            return render_template('results.html', tables = detailsInfo)
        if(homeQuery != None):
            return render_template('base.html', title="sample html")
        if secondQuery != None:
            sum = ast.literal_eval(request.form.get("tunnel"))
            rele1 = request.form.get("rele" + sum[0][0])
            rele2 = request.form.get("rele" + sum[1][0])
            rele3 = request.form.get("rele" + sum[2][0])
            relevant = []
            irr = []
            if rele1 != None:
                if rele1 == 'Relevant':
                    relevant.append(sum[0])
                else:
                    irr.append(sum[0])
                if rele2 != None:
                    if rele2 == 'Relevant':
                        relevant.append(sum[1])
                    else:
                        irr.append(sum[1])
                    if rele3 != None:
                        if rele3 == 'Relevant':
                            relevant.append(sum[2])
                        else:
                            irr.append(sum[2])
                        return render_template('catalogue.html', tables = rocchio(sum, relevant, irr))
            return render_template('catalogue.html', tables = sum)
        else:
            return render_template('twostep.html', tables=(output(query, sql_search(query2, query3, query4), invind, idf)))
    return render_template('base.html', title="sample html")


app.run(debug=True)