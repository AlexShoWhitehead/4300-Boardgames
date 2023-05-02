import pandas as pd
import json
import numpy as np
import re
import math

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

def build_inverted_index(msgs):
    d  ={}
    for i in range(len(msgs)):
        unique_words = set(msgs[i]['toks'])
        for word in unique_words:
            if word in d.keys():
                d[word].append( (i, msgs[i]['toks'].count(word)) )
            else:
                d[word] = [(i, msgs[i]['toks'].count(word))]
    return d

def compute_idf(inv_idx, n_docs, min_df=10, max_df_ratio=0.95):
    idf_dict = {}

    for key in inv_idx.keys():
        if not(len(inv_idx[key]) < min_df or len(inv_idx[key])/n_docs > max_df_ratio):
            idf_dict.update({key : math.log(n_docs/(1 + len(inv_idx[key])), 2)})

    return idf_dict

def compute_doc_norms(index, idf, n_docs):
    norms = np.zeros(shape=[n_docs])
    for i in idf:
        for j in index[i]:
            norms[j[0]] += np.square(j[1] * idf[i])

    for r in range(n_docs):
        norms[r] = (np.sqrt(norms[r]))

    return norms

def accumulate_dot_scores(query_word_counts, index, idf):
    doc_scores = {}

    for word in query_word_counts:
        for tup in index[word]:
            if tup[0] in doc_scores:
                if word in idf:
                    doc_scores[tup[0]] += idf[word] ** 2 * query_word_counts[word] * tup[1]
            else:
                if word in idf:
                    doc_scores.update({tup[0]: idf[word] ** 2 * query_word_counts[word] * tup[1]})
                else:
                    doc_scores.update({tup[0]: 0})


    return doc_scores

def get_word_counts(text):
  word_counts = {}
  tokens = tokenize(text)

  for word in tokens:
    if word in word_counts.keys():
      word_counts[word] += 1
    else:
      word_counts.update({word : 1})

  return word_counts

def index_search(query, index, idf, doc_norms, tokenizer, score_func=accumulate_dot_scores):
    results = []
    tokenized_query = tokenizer(query.lower())
    query_words = get_word_counts(query)

    dot_product_scores = score_func(query_words, index, idf)

    q_sum = 0
    for i in query_words:
      if i in idf:
        q_sum += np.square(query_words[i] * idf[i])
    q_norm = np.sqrt(q_sum)

    for doc_id in dot_product_scores.keys():
        norm_d = doc_norms[doc_id]
        numerator = dot_product_scores[doc_id]
        cos_score = numerator / np.dot(q_norm, norm_d)
        results.append( (cos_score, doc_id) )

    return sorted(results, reverse=True)

# finally we should be able to take in the query and return the most similar
# games
def output(query, database):
  game_data = json.loads(database)
  word_count = {}
  descriptions = []
  comments = []
  names = []
  images = []
  avg_ratings = []
  categories = []

  for game in range(len(game_data)): 
    descriptions.append(str(game_data[game]['qualitative_data']))
    comments.append(str(game_data[game]['comments']))
    names.append(str(game_data[game]['name']))
    images.append(str(game_data[game]['image_data']))
    avg_ratings.append(str(game_data[game]['rating_average']))
    categories.append(str(game_data[game]['categories']))

  doc_tokens = []

  for i in range(len(descriptions)):
    tokens = tokenize(descriptions[i])
    tokens += tokenize(comments[i])
    doc_tokens.append({'id' : i, 'toks' : tokens})

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

  inv_idx = build_inverted_index(doc_tokens)
  idf = compute_idf(inv_idx, len(doc_tokens))
  doc_norms = compute_doc_norms(inv_idx, idf, len(doc_tokens))
  query_word_counts = get_word_counts(query)
  dot_scores = accumulate_dot_scores(query_word_counts, inv_idx, idf)
  results = index_search(query, inv_idx, idf, doc_norms, tokenize, score_func=accumulate_dot_scores)

  #r_list is a list containing everyting we want
  ranked_list = []
  for i in range(3):
    index = results[i][1]
    sim_score = round(results[i][0], 3) 
    ranked_list = []
  for i in range(num_results):
    index = results[i][1]
    sim_score = round(results[i][0], 3)
    ranked_list.append(names[index] + " Sim score: " + str(sim_score) + " Average Ratings: " + average_ratings[index] +
                       " Categories : " + categories[index] + " Description : " + descriptions[index]
                       + " image url: " + images[index][images[index].index("'image':")+10 : len(images[index])-2])

    return ranked_list
    ranked_list.append(names[index] + " Sim score: " + str(sim_score) + " Average Ratings: " + avg_ratings[index] +
                       " Categories : " + categories[index] + " Description : " + descriptions[index]
                       + " image url: " + images[index][images[index].index("'image':")+10 : len(images[index])-2])

  return ranked_list

