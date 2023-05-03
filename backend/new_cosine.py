import pandas as pd
import numpy as np
import math
import json
import re

def tokenize(text):
    return re.findall(r"[a-zA-z]+", text.lower())

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

def get_results(results, names, average_ratings, categories, descriptions, images, num_results = 20):
  ranked_list = []
  for i in range(num_results):
    index = results[i][1]
    sim_score = round(results[i][0], 3)
    ranked_list.append([names[index], str(sim_score), average_ratings[index], categories[index], descriptions[index], images[index][images[index].index("'image':")+10 : len(images[index])-2]])

  return ranked_list

def output(query, database):
    game_data = pd.read_json(str(json.loads(database)[0]))
    #the below code parses the 'qualitative_data' column and makes a new column called 'description'
    game_data['description'] = game_data['qualitative_data']

    for i in range(1, len(game_data['id'])):
      if "description" in game_data['description'][i]:
        desc_index = game_data['description'][i].index('description')
        partial_string = game_data['description'][i][desc_index+15:]
        game_data['description'][i] = partial_string[:partial_string.index("families")-4]
      else:
        game_data['description'][i] = ""

    #this chunk just takes the df columns and makes them np arrays
    names = game_data['name'].astype('string').to_numpy()
    descriptions = game_data['description'].astype('string').to_numpy()
    comments = game_data['comments'].astype('string').to_numpy()
    images = game_data['image_data'].astype('string').to_numpy()
    average_ratings = game_data['rating_average'].astype('string').to_numpy()
    categories = game_data['categories'].astype('string').to_numpy()
    images = game_data['image_data'].astype('string').to_numpy()

    doc_tokens = []

    for i in range(len(descriptions)):
      tokens = tokenize(descriptions[i])
      tokens += tokenize(comments[i])
      doc_tokens.append({'id' : i, 'toks' : tokens})

    #these three values can all be precomputed, they don't rely on the query
    inv_idx = build_inverted_index(doc_tokens)
    idf = compute_idf(inv_idx, len(doc_tokens))
    doc_norms = compute_doc_norms(inv_idx, idf, len(doc_tokens))

    #this gets the results (the variable called results is NOT what we want to display)
    query_word_counts = get_word_counts(query)
    dot_scores = accumulate_dot_scores(query_word_counts, inv_idx, idf)
    results = index_search(query, inv_idx, idf, doc_norms, tokenize, score_func=accumulate_dot_scores)

    #r_list is a list containing everyting we want
    r_list = get_results(results, names, average_ratings, categories, descriptions, images)

    return r_list
