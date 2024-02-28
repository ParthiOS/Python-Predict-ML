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

