# This is the start of the prototype
import pandas as pd
import numpy as np
import re


# Game_Data.csv is in the shared drive
game_data = pd.read_csv('datasets/Game_Data.csv').dropna()

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

descriptions = game_data['Description'].astype('string').to_numpy()
names = game_data['Name'].astype('string').to_numpy()

for description in descriptions:
  token_list = tokenize(description)
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

def get_ranked_list(query, num_of_results = 5):
  sim_scores = np.empty(len(names))

  for i in range(len(description_vectors)):
    sim_scores[i] = cosine_sim(query, description_vectors[i])

  sorted_index = np.argsort(sim_scores)

  ranked_list = []
  for i in range(num_of_results):
    ranked_list.append(names[sorted_index[len(sorted_index) - 1 - i]])

  return ranked_list

# finally we should be able to take in the query and return the most similar
# games

def output(q):
  query = vectorize(q, good_types, tokenize)

  ranked_list = get_ranked_list(query)

  return ranked_list