# nbaPredict.py - Predicts results of NBA games on a specified date
# Call makeInterpretPrediction with current date, season, and start date of season to run predictions

import pickle
import pandas as pd

from matchups import curr_matchups

from model import create_mean_sd_dicts, z_differential, set_work_dir
from all_stats import all_stats
from get_team_stats import get_team_stats



# Returns list of games with Z-Score differentials between teams to be put into a Pandas dataframe
# startDate & endDate should be 'mm/dd/yyyy' form
def curr_game_df(dailyGames, meanDict, standardDeviationDict, startDate, endDate, season):

    fullDataFrame = []

    for homeTeam,awayTeam in dailyGames.items():

        homeTeamStats = get_team_stats(homeTeam, startDate, endDate, season)
        awayTeamStats = get_team_stats(awayTeam, startDate, endDate, season)

        currentGame = [homeTeam,awayTeam]

        for stat,statType in all_stats.items():  # Finds Z Score Dif for stats listed above and adds them to list
            zScoreDif = z_differential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
            currentGame.append(zScoreDif)

        fullDataFrame.append(currentGame)  # Adds this list to list of all games on specified date

    return(fullDataFrame)


# Returns a list
# Index 0 is the dailyGames in dict form {Home:Away}
# Index 1 is a list with the prediction probabilities for each game [[lossProb, winProb]]
# currentDate should be in form 'mm/dd/yyyy' and season in form 'yyyy-yy'
def predict_curr_games(currentDate, season, startOfSeason):

    dailyGames = curr_matchups(currentDate)  # Gets all games for specified date
    meanDict, standardDeviationDict = create_mean_sd_dicts(startOfSeason, currentDate, season)
    dailyGamesList = curr_game_df(dailyGames, meanDict, standardDeviationDict, startOfSeason, currentDate, season)

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


# Returns the percent chance that the home team will defeat the away team for each game
# gamesWithPredictions should be in form [dailyGames, predictionsList]
def interpret_pred(gamesWithPredictions):

    dailyGames = gamesWithPredictions[0]  # Dict holding daily matchups
    probabilityPredictions = gamesWithPredictions[1]  # List of lists holding probs of loss/win for home team

    for gameNum in range(len(probabilityPredictions)):  # Loops through each game
        winProb = probabilityPredictions[gameNum][1]
        winProbRounded = round(winProb,4)
        winProbPercent = "{:.2%}".format(winProbRounded)  # Formulates percent chance that home team wins

        homeTeam = list(dailyGames.keys())[gameNum]
        awayTeam = list(dailyGames.values())[gameNum]

        print('The ' + homeTeam   + ' winning against ' + awayTeam + ' prob is -> ' +  winProbPercent + '.')


# Fetches games on set date and returns predictions for each game
# currentDate/startOfSeason should be in form 'mm/dd/yyyy' and season in form 'yyyy-yy'
# Start of 2019-20 season was 10/2/2019
def make_pred(currentDate, season, startOfSeason):

    set_work_dir('SavedModels')

    print('Predictions for ' + currentDate + ':')
    predictions = predict_curr_games(currentDate, season, startOfSeason)
    interpret_pred(predictions)


