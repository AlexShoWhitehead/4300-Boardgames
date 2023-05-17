import boardgamegeek
import csv
import pandas as pd
import time
import ast

'''
code to get more than the default 100 comments
'''
CSV_PATH = 'datasets/master_database_cleaned.csv'

COMMENT_BOOL = True
RETRY_MAX = 5
DELAY_SEC = 60

bgg = boardgamegeek.BGGClient()


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


def update_comments(df, game, idx):
    comments = []
    for c in range(len(game.comments)):
        this_comment = {}
        comment = game.comments[c]
        this_comment['username'] = comment.username
        this_comment['rating'] = comment.rating
        this_comment['comment'] = comment.comment

        comments.append(this_comment)
    df.iloc[idx, df.columns.get_loc('comments')] = str(comments)
    df.iloc[idx, df.columns.get_loc('users_commented')] = int(len(game.comments))


def main():
    log = open('log_COMMENTS.txt', 'w')
    log.write('SCRIPT STARTED AT ' + str(time.strftime("%H:%M:%S", time.localtime())) + '\n')

    df = make_dataframe('datasets/master_database.csv', ';')

    for index, row in df.iterrows():
        if int(row['users_commented']) >= 100:
            print(index, row['name'].upper())

            try:
                print('  # comments: ' + str(row['users_commented']))
                game = bgg.game(game_id=row['id'], comments=True, progress=True)
                update_comments(df, game, index)
            except:
                log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
                          ': ERROR could not get comments for ' + row['name'] +
                          ' at index ' + str(index) + '. Most likely cause: request timeout. \n')
                print("ERROR at index " + str(index) + " for game " + row['name'])

    log.write(str(time.strftime("%H:%M:%S", time.localtime())) + ': COMPLETED. Closing log\n')
    log.close()
    df.to_csv("datasets/master_database_cleaned.csv", ';', index=False)



main()