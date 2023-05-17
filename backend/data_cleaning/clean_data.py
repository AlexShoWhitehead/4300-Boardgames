import csv
import pandas as pd
import ast
import re
from unidecode import unidecode



def make_dataframe(csv_path, delimiter):
    rows = []
    with open(csv_path, newline='', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_ALL)
        #next(reader, None)
        for row in reader:
            for col in range(len(row)):
                row[col].replace("â€™", "'")
                row[col].replace("Ä", "A")

            rows.append(row)
        csvfile.close()

    df = pd.DataFrame(rows)
    df.columns = df.iloc[0]
    df = df[1:]

    return df

def clean_complexity_ranking(df):
    df['complexity_average'] = df['complexity_average'].str.replace(',', '.').astype(float)
    return df


def remove_games_no_id(df):
    return df[df.iloc[:,0] != ""]


def remove_games_no_data(df):
    return df[df['qualitative_data'] != ""]


def get_dup_ids(df):
    sorted_df = df.sort_values(by=['id'])
    data= sorted_df[sorted_df['id'].duplicated(keep=False)]
    data.to_csv('duplicate_games.csv', index=True)


def remove_df_rows(df, rows_to_remove_list):
    removed_df = df.drop(labels=rows_to_remove_list, axis=0)
    return removed_df


def remove_games_by_desc(df, min_num_words):
    for index, row in df.iterrows():
        qual_data = ast.literal_eval(row['qualitative_data'])
        description = qual_data['description'].strip().replace('\n', '').split(' ')
        if len(description) < min_num_words:
            df = df.drop(labels=index, axis=0)

    return df

def remove_games_below_rating(df, rating):
    return df[df['rating_average'].astype(float) > rating]


def remove_games_by_num_comments(df, min_comments):
    df['users_commented'] = pd.to_numeric(df['users_commented'])
    return df[df['users_commented'] > min_comments]


def remove_games_not_english(df):
    for index, row in df.iterrows():
        name = row['name']
        english_check = re.compile(r'[a-z]')
        row['name'] = unidecode(row['name'])
        comments = row['comments']
        print(re.findall('[;]', comments))

        try:
            description = ast.literal_eval(row['qualitative_data'])['description'].strip()
        except:
            print("error at row ", index, ": ", row['name'])



def save_csv(df, csv_path):
    df.to_csv(csv_path, ';')

def clean_desc_comments(df):
    for index, row in df.iterrows():
        row['name'] = unidecode(row['name'])

def replace_i_with_j(df, i, j):
    for index, row in df.iterrows():
        qualitative_data = ast.literal_eval(row['qualitative_data'])
        qualitative_data['description'] = qualitative_data['description'].strip().replace(i, j)
        alt_names = qualitative_data['alternative_names']
        for c in range(len(alt_names)):
            alt_names[c] = alt_names[c].replace(i, j)
        qualitative_data['alternative_names'] = alt_names

        row['qualitative_data'] = str(qualitative_data)
        row['name'] = row['name'].replace(i, j)
        comments = ast.literal_eval(str(row['comments']))
        for c in range(len(comments)):
            comments[c]['username'] = comments[c]['username'].replace(i, j)
            comments[c]['comment'] = comments[c]['comment'].replace(i, j)
        row['comments'] = comments

def main():

    df = make_dataframe('datasets/master_database.csv', ';')
    df = remove_games_no_id(df)
    pd.options.display.max_columns = None
    #remove_games_not_english(df)



    print('original dataset', df.shape)

    df = remove_games_no_data(df)
    print('post removing lack of data', df.shape)

    df = remove_df_rows(df, [20344, 18139, 3898, 20359, 20360, 20358, 4248])
    print('post removing duplicates', df.shape)
    df = remove_games_by_desc(df, 10)
    #df = df.iloc['name']

    df = clean_complexity_ranking(df)
    print('post removing short descriptions', df.shape)
    df = remove_games_by_num_comments(df, 10)
    print('post removing few comments', df.shape)

    df = remove_games_below_rating(df, 5.0)
    print('post removing games under 5/10', df.shape)
    df = df

    # df['name_engl'] = unidecode(df['name'])
    # print(df['name_engl'])
    #df = df.str.encode('ascii', 'ignore').str.decode('ascii')
    df = df.replace("Ä", "A", regex=True)
    df = df.replace(';', ',', regex=True)
    df.replace({r'[^\x00-\x7F]+': ''}, regex=True, inplace=True)
    #df.name.replace({r'[^\x00-\x7F]+': ''}, regex=True, inplace=True)


    remove_games_not_english(df)
    df.to_csv("datasets/master_database_cleaned.csv", ';', index=False)


    df = make_dataframe('datasets/master_database_cleaned.csv', ';')

    replace_i_with_j(df, r"\'", r"`")
    replace_i_with_j(df, "'", "`")
    replace_i_with_j(df, r'"', '`')
    #print(df.columns)
    df.to_csv("datasets/master_database_quoteless.csv", ';', index=False)


main()