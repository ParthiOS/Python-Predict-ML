# getDailyMatchups.py - Finds the daily NBA games

from nba_api.stats.endpoints import leaguegamelog, scoreboard
from teams import teams



# Enter a date in the format mm/dd/yyyy
def curr_matchups(date):


    dailyMatchups = scoreboard.Scoreboard(league_id='00', game_date=date, timeout=120)
    dailyMatchupsDict = dailyMatchups.get_normalized_dict()
    listOfGames = dailyMatchupsDict['GameHeader']

    homeAwayDict = {}

    for game in listOfGames: 

        homeTeamID = game['HOME_TEAM_ID']

        for team, teamID in teams.items():  
            if teamID == homeTeamID:
                homeTeamName = team

        awayTeamID = game['VISITOR_TEAM_ID']

        for team, teamID in teams.items():  
            if teamID == awayTeamID:
                awayTeamName = team

        homeAwayDict.update({homeTeamName:awayTeamName})

    return homeAwayDict

# Enter a date in the format mm/dd/yyyy and season in the format yyyy-yy
def past_matchups(date, season):

    
    dailyMatchups = leaguegamelog.LeagueGameLog(season=season, league_id='00', season_type_all_star='Regular Season', date_from_nullable=date,date_to_nullable=date,timeout=60)
    dailyMatchupsDict = dailyMatchups.get_normalized_dict()
    listOfTeams = dailyMatchupsDict['LeagueGameLog']

    winLossList = []
    homeAwayDict = {}
    for i in range(0,len(listOfTeams),2):  
        if '@' in listOfTeams[i]['MATCHUP']: 
            awayTeam = listOfTeams[i]['TEAM_NAME']
            homeTeam = listOfTeams[i+1]['TEAM_NAME']

            winLossList.append(listOfTeams[i+1]['WL'])  

        else:
            awayTeam = listOfTeams[i+1]['TEAM_NAME']
            homeTeam = listOfTeams[i]['TEAM_NAME']

            winLossList.append(listOfTeams[i]['WL']) 

        homeAwayDict.update({homeTeam:awayTeam})  

    matchupsResultCombined = [homeAwayDict, winLossList] 
    return(matchupsResultCombined)




