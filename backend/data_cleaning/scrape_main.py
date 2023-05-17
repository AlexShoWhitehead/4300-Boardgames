import boardgamegeek
import csv
import pandas as pd
import time

'''
main scrape of data
'''

CSV_PATH = 'bgg_dataset.csv'
SHEET_PREFIX = 'sheet_'
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


log = open('log.txt', 'w')
log.write('SCRIPT STARTED AT '+ str(time.strftime("%H:%M:%S", time.localtime()))+ '\n')


df = pd.DataFrame(rows)
df.columns = df.iloc[0].str.lower()
df = df[1:]
df.rename(columns={'year published' : 'year_published', 
                   'min players' : 'min_players',
                   'max players' : 'max_players',
                   'play time' : 'play_time',
                   'min age' : 'min_age',
                   'users rated' : 'users_rated',
                   'rating average' : 'rating_average',
                   'bgg rank' : 'bgg_rank',
                   'complexity average' : 'complexity_average',
                   'owned users' : 'owned_users'}, inplace=True)

df['categories'] = ''
df['statistical_data'] = ''
df['qualitative_data'] = ''
df['image_data'] = ''
df['users_commented'] = ''
df['comments'] = ''

def get_game_by_name(name):
    try:
        return bgg.game(name, comments=COMMENT_BOOL, progress=COMMENT_BOOL)
    except:
        log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
                  'ERROR getting game '+ name + '\n')
        print('ERROR failed to get game by name', name)
        return None


def get_game_by_id(id, name):
    try:
        g = bgg.game(game_id=id, comments=COMMENT_BOOL, progress=COMMENT_BOOL)
        return g
    except:
        print('ERROR failed to get game by ID.')
        # log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
        #           ': ERROR getting game with id ' + id +
        #           '. Attempting to retrieve by name '+ name+'\n')
        # get_game_by_name(name)
        return None


def make_stat_dict(game):
    statistical_data = {}
    try:
        stats = game._stats
        statistical_data['rating_bayes_average'] = stats.rating_bayes_average
        statistical_data['rating_stdev'] = stats.rating_stddev
        statistical_data['rating_median'] = stats.rating_median
        statistical_data['rating_num_weights'] = stats.rating_num_weights
        statistical_data['rating_average_weight'] = stats.rating_average_weight
    except:
        log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
                  ': ERROR constructing statistical dictionary for game '+ str(game.name) + '\n')
        print('ERROR could not construct statistical dictionary for game', game.name)
    return statistical_data

        


def make_qual_dict(game):
    qualitative_data = {}
    try:
        qualitative_data['alternative_names'] = game.alternative_names
        qualitative_data['description'] = str(game.description)
        qualitative_data['families'] = game.families

        expansions_list = []
        expands_list = []
        if len(game.expansions) > 0:
            expansions_list = [exp.name for exp in game.expansions]
        if len(game.expands) > 0:
            expands_list = [exp.name for exp in game.expands]
        
        qualitative_data['is_expansion'] = game.expansion
        qualitative_data['expansions'] = expansions_list
        qualitative_data['expands'] = expands_list
    except:
        log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
                  ': ERROR constructing qualitative dictionary for game '+ str(game.name) + '\n')
        print('ERROR could not construct qualitative dictionary for game', game.name)
    return qualitative_data

def make_img_dict(game):
    img_dict = {}
    try:
        img_dict['thumbnail'] = game.thumbnail
        img_dict['image'] = game.image
    except:
        log.write(str(time.strftime("%H:%M:%S", time.localtime()))+
                  ': ERROR constructing image dictionary for game'+ str(game.name) + '\n')
        print('ERROR could not construct image dictionary for game', game.name)

    return img_dict

def make_row(df, i):
    print(i, ': ', df.iloc[i, 1])
    game = get_game_by_id(df.iloc[i, 0], df.iloc[i, 1])

    if game != None:

        # updating existing fields
        df.iloc[i, df.columns.get_loc('users_rated')] = game._stats.users_rated
        df.iloc[i, df.columns.get_loc('rating_average')] = game._stats.rating_average
        df.iloc[i, df.columns.get_loc('bgg_rank')] = game.bgg_rank
        df.iloc[i, df.columns.get_loc('owned_users')] = game.users_owned
        df.iloc[i, df.columns.get_loc('mechanics')] = str(game.mechanics)
        df.iloc[i, df.columns.get_loc('categories')] = str(game.categories)
        df.iloc[i, df.columns.get_loc('rating_average')] = game._stats.rating_average
        df.iloc[i, df.columns.get_loc('users_commented')] = game.users_commented

        df.iloc[i, df.columns.get_loc('statistical_data')] = str(make_stat_dict(game))
        df.iloc[i, df.columns.get_loc('qualitative_data')] = str(make_qual_dict(game))
        df.iloc[i, df.columns.get_loc('image_data')] = str(make_img_dict(game))

        comments = []

        for c in range(len(game.comments)):
            this_comment = {}
            comment = game.comments[c]
            this_comment['username'] = comment.username
            this_comment['rating'] = comment.rating
            this_comment['comment'] = comment.comment

            comments.append(this_comment)


        df.iloc[i, df.columns.get_loc('comments')] = str(comments)
    else:
        log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
                  ': ERROR could not parse game with id ' + str(df.iloc[i, 0]) +
                  ' at row ' + str(i) + '. Most likely cause: request timeout. \
                    see request_and_parse_xml(). \n')
        print('ERROR could not parse game with id', df.iloc[i, 0], 'at row ', i)




start_idx = 0
while start_idx < len(df):
    this_sheet_path = SHEET_PREFIX + str(int(start_idx/SHEET_SIZE)).zfill(2) + '.csv'
    print("OPENING "+ this_sheet_path)
    log.write(str(time.strftime("%H:%M:%S", time.localtime())) + ': OPENING ' + this_sheet_path + '...\n')
    with open(this_sheet_path, 'w', newline='', encoding='UTF-8') as csvfile:
        writer =  csv.writer(csvfile)
        writer.writerow(df.columns)
        for i in range(start_idx, min(len(df), start_idx + SHEET_SIZE)):
            '''
            rtr = RETRY_MAX
            success_write = False
            while rtr >= 0:
                rtr -= 1
                try:
                    time.sleep(DELAY_SEC)
                    make_row(df, i)
                    writer.writerow(df.iloc[i])
                    rtr = -1
                    success_write = True
                except:
                    print('LONG DELAY starting')
                    time.sleep(DELAY_SEC*10)
                    log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
                                 ': ERROR could not write row '+ str(i) + 'of ' + this_sheet_path +
                                 ' for game ' + df.iloc[i, 1] + '. SKIPPING game.')
                    print("ERROR could not write row", i, 'for game', df.iloc[i, 1],'. Delay and  retry. Retries =', rtr)
                    continue
            if success_write == False:
                writer.writerow("")
            '''
            try:
                make_row(df, i)
                writer.writerow(df.iloc[i])
            except:
                log.write(str(time.strftime("%H:%M:%S", time.localtime())) +
                                 ': ERROR could not write row '+ str(i) + 'of ' + this_sheet_path +
                                 ' for game ' + df.iloc[i, 1] + '. SKIPPING game.')
                print("ERROR could not write row", i, 'for game', df.iloc[i, 1])

        start_idx = i+1
        log.write(str(time.strftime("%H:%M:%S", time.localtime())) + ': CLOSING '+ this_sheet_path + '\n')
        print("CLOSING "+ this_sheet_path)

        csvfile.close()

log.write(str(time.strftime("%H:%M:%S", time.localtime())) + ': COMPLETED. Closing log\n')
log.close()