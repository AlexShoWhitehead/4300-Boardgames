import boardgamegeek
import csv
import pandas as pd
import time

'''
manually fixing a few lines of the CSV
'''
CSV_PATH = 'bgg_dataset.csv'
SHEET_SIZE = 1000
COMMENT_BOOL = True
RETRY_MAX = 5
DELAY_SEC = 60

bgg = boardgamegeek.BGGClient()

rows = []
with open(CSV_PATH, newline='', encoding='UTF-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
        rows.append(row)
    csvfile.close()

log = open('log_FIXING.txt', 'w')
log.write('SCRIPT STARTED AT ' + str(time.strftime("%H:%M:%S", time.localtime())) + '\n')

df = pd.DataFrame(rows)
df.columns = df.iloc[0].str.lower()
df = df[1:]
df.rename(columns={'year published': 'year_published',
                   'min players': 'min_players',
                   'max players': 'max_players',
                   'play time': 'play_time',
                   'min age': 'min_age',
                   'users rated': 'users_rated',
                   'rating average': 'rating_average',
                   'bgg rank': 'bgg_rank',
                   'complexity average': 'complexity_average',
                   'owned users': 'owned_users'}, inplace=True)

df['categories'] = ''
df['statistical_data'] = ''
df['qualitative_data'] = ''
df['image_data'] = ''
df['users_commented'] = ''
df['comments'] = ''

ids = [(283150, 5691),
       (239930, 8354),
       (244817, 9228),
       (283153, 9329),
       (244433, 9391),
       (-1, 10776),
       (-1, 10835),
       (-1, 11152),
       (-1, 11669),
       (-1, 12649),
       (-1, 12764),
       (-1, 13282),
       (-1, 13984),
       (-1, 14053),
       (171912, 14143),
       (15998, 14426),
       (39834, 14480),
       (-1, 14663),
       (237082, 15637),
       (-1, 16292),
       (-1, 17009),
       (-1, 18672),
       (-1, 19332),
       (-1, 19474),
       (-1, 20040)]

fixed_ids = [
            156546,  # MONIKERS: redirected
            239930,  # TOUR OPERATOR: timeout
            244817,  # FARMINI: timeout
            255249,  # MONIKERS MORE MOIKERS: redirected
            242879,  # LADRILLAZO: redirected
            1991,    # Ace of Aces Jet Eagle: no ID
            413,     # Die Erben von Hoax: no ID
            11113,   # Rommel in North Africa: The War in the Desert: no ID
            143663,  # Migration: A Story of Generations: no ID
            54501,   # Die Insel der steinernen Wachter: no ID
            168077,  # Dragon Ball Z TCG (2014 edition): no ID
            170337,  # Dwarfest: no ID
            25999,   # Hus: no ID
            27227,   # Contrario 2: no ID
            88922,   # Clue Suspect: redirect
            2607,    # Topoly: redirect
            344,     # classic art: redirect
            198886,  # Warage: Extended Edition: no ID
            196379,  # shit happens: redirecct
            73574,   # Rainbow
            148211,  # Sexy, el juego del arte del flirteo
            269573,  # dracarys-dice
            8173,    # Battleship: Tactical Capital Ship Combat 1925-1945
            316555,  # The Umbrella Academy Game
            15804]   # hidden Conflict


def get_game_by_id(id):
    try:
        g = bgg.game(game_id=id, comments=COMMENT_BOOL, progress=COMMENT_BOOL)
        return g
    except:
        print('ERROR failed to get game by ID (id='+id+')')
        # log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
        #           ': ERROR getting game with id ' + id +
        #           '. Attempting to retrieve by name '+ name+'\n')
        # get_game_by_name(name)
        return None

def make_row(df, game_id, df_row):
    game = get_game_by_id(game_id)

    if game != None:

        # updating existing fields
        df.iloc[df_row, 0] = game_id
        df.iloc[df_row, df.columns.get_loc('name')] = str(game.name)
        df.iloc[df_row, df.columns.get_loc('users_rated')] = game._stats.users_rated
        df.iloc[df_row, df.columns.get_loc('rating_average')] = game._stats.rating_average
        df.iloc[df_row, df.columns.get_loc('bgg_rank')] = game.bgg_rank
        df.iloc[df_row, df.columns.get_loc('owned_users')] = game.users_owned
        df.iloc[df_row, df.columns.get_loc('mechanics')] = str(game.mechanics)
        df.iloc[df_row, df.columns.get_loc('categories')] = str(game.categories)
        df.iloc[df_row, df.columns.get_loc('rating_average')] = game._stats.rating_average
        df.iloc[df_row, df.columns.get_loc('users_commented')] = game.users_commented

        df.iloc[df_row, df.columns.get_loc('statistical_data')] = str(make_stat_dict(game))
        df.iloc[df_row, df.columns.get_loc('qualitative_data')] = str(make_qual_dict(game))
        df.iloc[df_row, df.columns.get_loc('image_data')] = str(make_img_dict(game))

        comments = []

        for c in range(len(game.comments)):
            this_comment = {}
            comment = game.comments[c]
            this_comment['username'] = comment.username
            this_comment['rating'] = comment.rating
            this_comment['comment'] = comment.comment

            comments.append(this_comment)

        df.iloc[df_row, df.columns.get_loc('comments')] = str(comments)
    else:
        log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
                  ': ERROR could not parse game with id ' + str(df.iloc[df_row, 0]) +
                  ' at row ' + str(df_row) + '. Most likely cause: request timeout. \
                    see request_and_parse_xml(). \n')
        print('ERROR could not parse game with id', df.iloc[df_row, 0], 'at row ', df_row)


this_sheet_path = 'datasets/sheet_missed.csv'
print("OPENING " + this_sheet_path)
with open(this_sheet_path, 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(df.columns)
    for i in range(len(ids)):
        this_id = fixed_ids[i]
        this_row = ids[i][1]
        print('id', this_id)
        print('row', this_row)
       # try:
        make_row(df, this_id, this_row)
        writer.writerow(df.iloc[this_row])
        # except:
        #     log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
        #               ': ERROR could not write row ' + str(this_row) + 'of ' + this_sheet_path +
        #               ' for game ' + df.iloc[this_row, 1] + '. SKIPPING game.\n')
        #     print("ERROR could not write row", this_row, 'for game', df.iloc[this_row, 1])

log.write(str(time.strftime("%H:%M:%S", time.localtime())) + ': COMPLETED. Closing log\n')
log.close()