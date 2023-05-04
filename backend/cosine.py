import pandas as pd
import json
import numpy as np
import re
import csv

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

def tokenize(text):
    """Returns a list of words that make up the text.
    Note: for simplicity, lowercase everything.
    Requirement: Use Regex to satisfy this function
    Params: {text: String}
    Returns: List
    """
    return re.findall(r"[a-zA-z]+", text.lower())
# I want to make a dictionary containing every word in the descriptions and their counts

word_count = {}
token_list = []

# Now I'll make a function that takes in text and turns it into a vector
# representation of good types

def vectorize(text, good_types, tokenizer):
  token_list = tokenizer(text)
  vector = np.zeros(len(good_types))
  for word in token_list:
    if word in good_types:
      vector[good_types.index(word)] += 1
  return vector

def cosine_sim(query, vector):
  query_norm = np.linalg.norm(query)
  vector_norm = np.linalg.norm(vector)
  dot_product = np.dot(query, vector)

  return dot_product / (query_norm * vector_norm)

def get_ranked_list(query, names, description_vectors, descriptions, comments, images, average_ratings, categories, num_of_results = 20):
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
def output(query, database):
  game_data = database
  names = game_data['name'].astype('string').to_numpy()
  descriptions = game_data['description'].astype('string').to_numpy()
  comments = game_data['comments'].astype('string').to_numpy()
  images = game_data['image_data'].astype('string').to_numpy()
  average_ratings = game_data['rating_average'].astype('string').to_numpy()
  categories = game_data['categories'].astype('string').to_numpy()
  images = game_data['image_data'].astype('string').to_numpy()

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

  good_types = []
  for word in word_count.keys():
    if word_count[word] >= 0:
      good_types.append(word)
  good_types.sort()
  query = vectorize(query, good_types, tokenize)

  description_vectors = []
  for description in descriptions:
    description_vectors.append(vectorize(description, good_types, tokenize))

  return get_ranked_list(query, names, description_vectors, descriptions, comments, images, average_ratings, categories, num_of_results = 3)
