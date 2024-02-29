# make working directory relative to where program is located
import os
import pickle
import pandas as pd 
from sklearn import  metrics
from apply_stats import *
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from possible_stats import possibleStats
from matchups import past_matchups
from datetime import timedelta, date

def set_work_dir(directoryName):

    program_dir = os.path.dirname(os.path.abspath(__file__))

    new_work_dir = os.path.join(program_dir, directoryName)

    os.chdir(new_work_dir)

def z_difference(stat_home, stat_away, mean, standard_dev):


    # find the difference in z scores between the home and away teams
    home_z = bas_adv_z(stat_home, mean, standard_dev)
    away_z = bas_adv_z(stat_away, mean, standard_dev)

    diff_z = home_z - away_z
    return diff_z

def put_into_df_list(daily_games, mean_dict, stand_dev_dict, start, end, season):
    
    df = []
    results = daily_games[1]
    game_num = 0

    for home, away in daily_games[0].items():
        home_stats = get_team_stats(home, start, end, season)
        away_stats = get_team_stats(away, start, end, season)   
        curr_game = [home, away]
        for stat, type in possibleStats.items():
            z_diff = z_difference(home_stats[stat], away_stats[stat], mean_dict[stat], stand_dev_dict[stat])
            curr_game.append(z_diff)
        


        if results[game_num] == 'W':
            result = 1
        else:
            result = 0

        
        curr_game.append(result)

        game_num += 1

        print(curr_game)
        df.append(curr_game)

    return df




def create_mean_sd_dict(start, end, season):

    mean_dict = {}
    sd_dict = {}

    for stat, stype in possibleStats.items():

        # gather the stats and put into dictionary
        
        
        stat_mean = bas_adv_mean(start, end, stat, stype, season)
        mean_dict.update({stat: stat_mean})
        stat_sd = bas_adv_stand_dev(start, end, stat, stype, season)
        sd_dict.update({stat: stat_sd})
    # put mean and sd into this big dict
    big_dict = []
    big_dict.append(mean_dict)
    big_dict.append(sd_dict)

    return big_dict

def get_range(start, end):

    for d in range(int((end - start).days)):
        yield start + timedelta(d)

def create_training_set(s_year, s_month, s_day, e_year, e_month, e_day, season, s_season):

    matches = []
    start = date(s_year,s_month, s_day) # rearrange to be in the proper format if needed check later if causing an error with parameters
    end = date(e_year, e_month, e_day)

    
    
    for d in get_range(start, end):
        curr_date = d.strftime("%m/%d/%Y")
        print(curr_date)
        prev_day = d - timedelta(days = 1)
        prev_day_form = prev_day.strftime("%m/%d/%Y")

        mean_sd_dict = create_mean_sd_dict(s_season, prev_day_form, season)
        mean_dict = mean_sd_dict[0]
        sd_dict = mean_sd_dict[1]

        todays_games = past_matchups(curr_date, season)
        todays_games_stat_list = put_into_df_list(todays_games, mean_dict, sd_dict, s_season, prev_day_form, season)
        
        for game in todays_games_stat_list:
            game.append(curr_date)
            matches.append(game)

        print(matches)
        return matches

    

def create_df(games_list):

    games = pd.DataFrame(
        games_list, columns = ['Home', 'Away', 'W_PCT', 'REB', 'TOV', 'PLUS_MINUS',
                                'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'Result', 'Date']
    )

    print(games) 
    return games


def perform_regression(df):
    cols = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    X = df[cols]
    y = df.Result 



    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, shuffle = True)

    model = LogisticRegression()

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    c_matrix = metrics.confusion_matrix(y_test, y_pred)

    print('Info:')

    for i in range(len(cols)):
        coeff = model.coef_
        curr_col = cols[i]
        curr_coeff = coeff[0][i]

        print(curr_col + ':' + str(curr_coeff))

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))

    print('----------------------------------')

    print('Confusion Matrix:')
    print(c_matrix)


def saveModel(model, filename):

    # Change to where you want to save the model
    set_work_dir('Models')

    with open(filename, 'wb') as file:
        pickle.dump(model, file)

def createModel(startYear=None, startMonth=None, startDay=None, endYear=None, endMonth=None, endDay=None, season='2018-19', startOfSeason = '10/16/2018', filename='model.pkl'):

    allGames = create_training_set(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startOfSeason)  # Unnecessary if using data from CSV file

    allGamesDataframe = create_df(allGames)  # Unnecessary if using data from CSV file

    #set_work_dir('Data')
    #allGamesDataframe = pd.read_csv('COMBINEDgamesWithInfo2016-19.csv')  # Should be commented out if needing to obtain data on different range of games
    #filename = 'model1.pkl'
    logRegModel = perform_regression(allGamesDataframe)

    saveModel(logRegModel, filename)


createModel(startYear=2023, startMonth=10, startDay=24, endYear=2024, endMonth=2, endDay=1, season='2023-24', startOfSeason = '10/24/2023', filename='model.pkl')