import csv
import pandas as pd
import ast

'''
script to replace characters in a csv file to avoid encoding/decoding issues
'''
def make_dataframe(csv_path, delimiter):
    rows = []
    with open(csv_path, newline='', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_ALL)
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
    df = make_dataframe('datasets/master_database_cleaned.csv', ';')

    replace_i_with_j(df, r"\'", r"`")
    replace_i_with_j(df, "'", "`")
    replace_i_with_j(df, r'"', '`')
    df.to_csv("datasets/master_database_quoteless.csv", ';', index=False)