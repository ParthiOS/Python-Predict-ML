
from nba_api.stats.endpoints import leaguedashteamstats
import statistics




def populate(startDate, endDate, stat,statType = 'Base', season='2018-19'):
    allTeamsInfo = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed='Per100Possessions',
                                                            measure_type_detailed_defense=statType,
                                                            date_from_nullable=startDate,
                                                            date_to_nullable=endDate,
                                                            season=season)
    allTeamsDict = allTeamsInfo.get_normalized_dict()
    allTeamsList = allTeamsDict['LeagueDashTeamStats']
    return allTeamsList

def bas_adv_mean(startDate, endDate, stat, statType = 'Base', season='2018-19'):

    
    
    allTeamsList = populate(startDate, endDate, stat, statType, season)
    
    specificStatAllTeams = []
    for i in range(len(allTeamsList)): 
        specificStatAllTeams.append(allTeamsList[i][stat])

    mean = statistics.mean(specificStatAllTeams) 
    return mean



def bas_adv_sd(startDate, endDate, stat,statType = 'Base', season='2018-19'):

    
    
    allTeamsList = populate(startDate, endDate, stat, statType, season)
    specificStatAllTeams = []
    for i in range(len(allTeamsList)): 
        specificStatAllTeams.append(allTeamsList[i][stat])

    standardDeviation = statistics.stdev(specificStatAllTeams)  
    return standardDeviation



def bas_adv_zscore(observedStat, mean, standardDeviation):

    zScore = (observedStat-mean)/standardDeviation  

    return(zScore)


#print(bas_adv_mean('10/28/2023','02/12/2024', 'PLUS_MINUS','Base', '2023-24'))