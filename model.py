

from apply_stats import bas_adv_mean, bas_adv_zscore, bas_adv_sd
from matchups import past_matchups
from get_team_stats import get_team_stats
from all_stats import all_stats


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pandas as pd
import pickle
import os
from datetime import timedelta, date


def set_work_dir(directoryName):

    programDirectory = os.path.dirname(os.path.abspath(__file__))
    newCurrentWorkingDirectory = os.path.join(programDirectory, directoryName)
    os.chdir(newCurrentWorkingDirectory)



def z_differential(observedStatHome, observedStatAway, mean, standardDeviation):

    homeTeamZScore = bas_adv_zscore(observedStatHome, mean, standardDeviation)
    awayTeamZScore = bas_adv_zscore(observedStatAway, mean, standardDeviation)

    differenceInZScore = homeTeamZScore - awayTeamZScore
    return differenceInZScore



def info_to_df(dailyGames, meanDict, standardDeviationDict, startDate, endDate, season):

    fullDataFrame = []
    gameNumber = 0  
    dailyResults = dailyGames[1]  

    for homeTeam,awayTeam in dailyGames[0].items():

        homeTeamStats = get_team_stats(homeTeam, startDate, endDate, season)
        awayTeamStats = get_team_stats(awayTeam, startDate, endDate, season)

        currentGame = [homeTeam,awayTeam]

        for stat,statType in all_stats.items():  
            zScoreDif = z_differential(homeTeamStats[stat], awayTeamStats[stat], meanDict[stat], standardDeviationDict[stat])
            currentGame.append(zScoreDif)

        if dailyResults[gameNumber] == 'W':  # Sets result to 1 if a win
            result = 1
        else:  # Sets result to 0 if loss
            result = 0

        currentGame.append(result)
        gameNumber += 1

        print(currentGame)
        fullDataFrame.append(currentGame)  

    return(fullDataFrame)


def date_range(startDate, endDate):

    for n in range(int ((endDate - startDate).days)):
        yield startDate + timedelta(n)



def create_mean_sd_dicts(startDate, endDate, season):

    meanDict = {}
    standardDeviationDict = {}

    for stat, statType in all_stats.items():
        statMean = bas_adv_mean(startDate, endDate, stat, statType, season)
        meanDict.update({stat: statMean})

        statStandardDeviation = bas_adv_sd(startDate, endDate, stat, statType, season)
        standardDeviationDict.update({stat: statStandardDeviation})

    bothDicts = []
    bothDicts.append(meanDict)
    bothDicts.append(standardDeviationDict)

    return bothDicts




def get_train_set(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startOfSeason):

    startDate = date(startYear, startMonth, startDay)
    endDate = date(endYear, endMonth, endDay)

    startDateFormatted = startDate.strftime("%m/%d/%Y")  
    allGames = []

    for singleDate in date_range(startDate, endDate):
        currentDate = singleDate.strftime("%m/%d/%Y") 
        print(currentDate)

        previousDay = singleDate - timedelta(days=1)
        previousDayFormatted = previousDay.strftime("%m/%d/%Y")

        meanAndStandardDeviationDicts = create_mean_sd_dicts(startOfSeason, previousDayFormatted, season)
        meanDict = meanAndStandardDeviationDicts[0]  
        standardDeviationDict = meanAndStandardDeviationDicts[1]  

        currentDayGames = past_matchups(currentDate, season)  
        currentDayGamesAndStatsList = info_to_df(currentDayGames, meanDict, standardDeviationDict, startOfSeason, previousDayFormatted, season)  

        for game in currentDayGamesAndStatsList: 
            game.append(currentDate)
            allGames.append(game)

    print(allGames)
    return(allGames)



def create_df(listOfGames):

    games = pd.DataFrame(
        listOfGames,
        columns=['Home', 'Away', 'W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'Result', 'Date']
    )

    print(games)
    return(games)



def performLogReg(dataframe):

    
    featureColumns = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    X = dataframe[featureColumns] 
    Y = dataframe.Result  

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, shuffle=True)
    logreg = LogisticRegression()

    logreg.fit(X_train, Y_train)  

    Y_pred = logreg.predict(X_test)

    confusionMatrix = metrics.confusion_matrix(Y_test, Y_pred)  

    
    print('Coefficient Information:')

    for i in range(len(featureColumns)):  

        logregCoefficients = logreg.coef_

        currentFeature = featureColumns[i]
        currentCoefficient = logregCoefficients[0][i]

        print(currentFeature + ': ' + str(currentCoefficient))

    print('----------------------------------')

    print("Accuracy:", metrics.accuracy_score(Y_test, Y_pred))
    print("Precision:", metrics.precision_score(Y_test, Y_pred))
    print("Recall:", metrics.recall_score(Y_test, Y_pred))

    print('----------------------------------')

    print('Confusion Matrix:')
    print(confusionMatrix)

    return logreg



def save_model(model, filename):

    
    set_work_dir('SavedModels')

    with open(filename, 'wb') as file:
        pickle.dump(model, file)



def createModel(startYear=None, startMonth=None, startDay=None, endYear=None, endMonth=None, endDay=None, season='2018-19', startOfSeason = '10/16/2018', filename='model.pkl'):

    allGames = get_train_set(startYear, startMonth, startDay, endYear, endMonth, endDay, season, startOfSeason)  # Unnecessary if CSV file

    allGamesDataframe = create_df(allGames)  # Unnecessary if CSV file

    #set_work_dir('Data')
    #allGamesDataframe = pd.read_csv('COMBINEDgamesWithInfo2016-19.csv')  # Should be commented out if new range

    logRegModel = (allGamesDataframe)
    
    save_model(logRegModel, filename)

#createModel(2023, 10, 28, 2024, 2, 14,'2023-24', '10/24/2023')