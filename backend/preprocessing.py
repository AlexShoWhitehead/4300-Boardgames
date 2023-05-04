import ast

def pre_inv (func, game_data_func, tokenize):
    game_data = game_data_func('datasets/master_database.csv', ';')
    descriptions = game_data['description'].astype('string').to_numpy()
    comments = game_data['comments'].astype('string').to_numpy()
    
    doc_tokens = []
    for i in range(len(descriptions)):
      tokens = tokenize(descriptions[i])
      tokens += tokenize(comments[i])
      doc_tokens.append({'id' : i, 'toks' : tokens})
    inv_ind = func(doc_tokens)
    
    with open('datasets/inv_ind.txt', 'w') as f:
       f.write(str(inv_ind))


def read_mat(file):
   with open(file, 'r') as f:
      lines = f.readlines()
      invind = ast.literal_eval(lines[0])
      
      return invind
