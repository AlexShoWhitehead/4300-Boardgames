import pandas as pd
import numpy as np
import re
import ast
import csv


def make_dataframe(csv_path, delimiter):
    rows = []
    with open(csv_path, newline='', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_ALL)
        next(reader, None)
        for row in reader:
            for col in range(len(row)):
                row[col].replace("â€™", "'")
            rows.append(row)
        csvfile.close()

    df = pd.DataFrame(rows)
    df.columns = df.iloc[0]
    df = df[1:]

    return df

description_data = pd.read_csv('datasets/Game_Data.csv')
game_data =  make_dataframe('datasets/master_database.csv', ';')
game_data = game_data.merge(description_data, on='name', how="right").drop("ID", axis='columns').dropna()

def tokenize(text):
    """Returns a list of words that make up the text.
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    Params: {text: String}
    Returns: List
    """
    return re.findall(r"[a-zA-z]+", text.lower())
# I want to make a dictionary containing every word in the descriptions and their counts

def filter(age=0, length=0, players=2): 
  """Filters out any games not fulfilling user needs
  Returns: filtered game_data  
  """
  strAge = str(age)
  strLength = str(length)
  strPlayers = str(players)

  ageFilter = game_data['min_age'] <= strAge
  lengthFilter = game_data['play_time'] >= strLength
  playersFilter = (game_data['min_players'] <= strPlayers)
  players2Filter = (game_data['max_players'] >= strPlayers)

  return game_data[ageFilter & lengthFilter & playersFilter & players2Filter]

game_data = filter()

word_count = {}

descriptions = game_data['description'].astype('string').to_numpy()
comments = game_data['comments'].astype('string').to_numpy()
names = game_data['name'].astype('string').to_numpy()

token_list = []

for description in descriptions:
  tokens = tokenize(description)
  for token in tokens:
    token_list.append(token)

for comment in comments:
  tokens = tokenize(comment)
  for token in tokens:
    token_list.append(token)

for word in token_list:
  if word in word_count.keys():
    word_count[word] += 1
  else:
    word_count.update({word: 1})

# Now I want to find the good types, since this is just a proto type
# I'm just going to say that words that occur more then 200 times are good
# In the future we should look at word frequencies to better fine tune which
# Words are considered good words
# These parameters can obviously be changed later
good_types = []
for word in word_count.keys():
  if word_count[word] >= 200:
    good_types.append(word)

good_types.sort()

# Now I'll make a function that takes in text and turns it into a vector
# representation of good types

def vectorize(text, good_types, tokenizer):
  token_list = tokenizer(text)
  vector = np.zeros(len(good_types))
  for word in token_list:
    if word in good_types:
      vector[good_types.index(word)] += 1
  return vector
# From here we can make vector representations for all the descriptions
description_vectors = []
for description in descriptions:
  description_vectors.append(vectorize(description, good_types, tokenize))

# ^ this code can take a while to run

# now that we have the descriton vectors, we will make a function that
# calculates the cosine similarity between a query and description vector

def cosine_sim(query, vector):
  query_norm = np.linalg.norm(query)
  vector_norm = np.linalg.norm(vector)
  dot_product = np.dot(query, vector)

  return dot_product / (query_norm * vector_norm)

# from here we will make a function that takes in a query and returns the top
# 20 results

images = game_data['image_data'].astype('string').to_numpy()
average_ratings = game_data['rating_average'].astype('string').to_numpy()
categories = game_data['rating_average'].astype('string').to_numpy()

def get_ranked_list(query, num_of_results = 20):
  sim_scores = np.empty(len(names))

  for i in range(len(description_vectors)):
    sim_scores[i] = cosine_sim(query, description_vectors[i])
  sorted_index = np.argsort(sim_scores)

  ranked_list = []
  for i in range(num_of_results):
    index = sorted_index[len(sorted_index) - 1 - i]
    return_vals = (names[index], descriptions[index], comments[index], images[index], average_ratings[index], categories[index])
    ranked_list.append(return_vals)

  return ranked_list

# finally we should be able to take in the query and return the most similar
# games
def output(q):
  query = vectorize(q, good_types, tokenize)

  ranked_list = get_ranked_list(query)

  return ranked_list