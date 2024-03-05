import pickle
import numpy as np
import pandas as pd

from matchups  import current_matchups
from model import create_mean_sd_dict, z_difference, set_work_dir
from possible_stats import possibleStats
from get_stats import get_team_stats

def dailyGamesDataFrame(dailyGames, meanDict, standardDeviationDict, startDate, endDate, season):

    fullDataFrame = []

    for homeTeam,awayTeam in dailyGames.items():

        homeTeamStats = get_team_stats(homeTeam, startDate, endDate, season)
        awayTeamStats = get_team_stats(awayTeam, startDate, endDate, season)

        currentGame = [homeTeam,awayTeam]

        for stat,statType in possibleStats.items():  # Finds Z Score Dif for stats listed above and adds them to list
            zScoreDif = z_difference(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
            currentGame.append(zScoreDif)

        fullDataFrame.append(currentGame)  # Adds this list to list of all games on specified date

    return(fullDataFrame)

def predictDailyGames(currentDate, season, startOfSeason):

    dailyGames = current_matchups(currentDate)  # Gets all games for specified date
    meanDict, standardDeviationDict = create_mean_sd_dict(startOfSeason, currentDate, season)
    dailyGamesList = dailyGamesDataFrame(dailyGames, meanDict, standardDeviationDict, startOfSeason, currentDate, season)

    # Pandas dataframe holding daily games and Z-Score differentials between teams
    gamesWithZScoreDifs = pd.DataFrame(
        dailyGamesList,
        columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
    )

    justZScoreDifs = gamesWithZScoreDifs.loc[:,'W_PCT':'TS_PCT']  # Slices only the features used in the model

    with open('model.pkl', 'rb') as file:  # Change filename here if model is named differently
        pickleModel = pickle.load(file)

    predictions = pickleModel.predict_proba(justZScoreDifs)  # Predicts the probability that the home team loses/wins

    gamesWithPredictions = [dailyGames, predictions]
    return gamesWithPredictions


