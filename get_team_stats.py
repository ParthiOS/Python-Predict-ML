

from teams import teams
from nba_api.stats.endpoints import teamdashboardbygeneralsplits




# startDate and endDate should be in format 'mm/dd/yyyy'
def get_team_stats(team, startDate, endDate, season='2019-20'):

    
    
    generalTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams[team], per_mode_detailed='Per100Possessions', date_from_nullable=startDate, date_to_nullable=endDate, season=season, timeout=120)
    generalTeamDict = generalTeamInfo.get_normalized_dict()
    generalTeamDashboard = generalTeamDict['OverallTeamDashboard'][0]

    
    winPercentage = generalTeamDashboard['W_PCT']
    rebounds = generalTeamDashboard['REB']
    turnovers = generalTeamDashboard['TOV']
    plusMinus = generalTeamDashboard['PLUS_MINUS']

    
    advancedTeamInfo = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams[team], measure_type_detailed_defense='Advanced', date_from_nullable=startDate, date_to_nullable=endDate, season=season, timeout=120)
    advancedTeamDict  = advancedTeamInfo.get_normalized_dict()
    advancedTeamDashboard = advancedTeamDict['OverallTeamDashboard'][0]

    
    offensiveRating = advancedTeamDashboard['OFF_RATING']
    defensiveRating = advancedTeamDashboard['DEF_RATING']
    trueShootingPercentage = advancedTeamDashboard['TS_PCT']

    # Put all the stats into a dictionary
    allStats = {
        'W_PCT':winPercentage,
        'REB':rebounds,
        'TOV':turnovers,
        'PLUS_MINUS':plusMinus,
        'OFF_RATING':offensiveRating,
        'DEF_RATING': defensiveRating,
        'TS_PCT':trueShootingPercentage,
    }

    return allStats
