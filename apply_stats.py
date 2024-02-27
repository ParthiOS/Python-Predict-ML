import statistics
from get_stats import get_team_stats

from nba_api.stats.endpoints import leaguedashteamstats


def bas_adv_mean(start, end, stat , type = 'Base', season = '2022-23'):
    
    teams_info = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed = 'Per100Possessions', measure_type_detailed_defense=type,
                                                        date_from_nullable=start, date_to_nullable=end, season=season)
    
    teams_dict = teams_info.get_normalized_dict()
    print(stat, teams_dict)
    teams_list = teams_dict['LeagueDashTeamStats']
    
    #gather the data into a dict then turn it into a list
    one_stat_teams = []
    # create a list and add every teams unique stat into the list
    for i in range(len(teams_list)):
        one_stat_teams.append(teams_list[i][stat])


    stat_mean = statistics.mean(one_stat_teams)
    return stat_mean
    

def bas_adv_stand_dev(start, end, stat , type = 'Base', season = '2023-24'):

    teams_info = leaguedashteamstats.LeagueDashTeamStats(per_mode_detailed = 'Per100Possessions', measure_type_detailed_defense=type,
                                                        date_from_nullable=start, date_to_nullable=end, season=season)
    
    teams_dict = teams_info.get_normalized_dict()
    teams_list = teams_dict['LeagueDashTeamStats']
    #gather the data into a dict then turn it into a list
    one_stat_teams = []
    # create a list and add every teams unique stat into the list
    for i in range(len(teams_list)):
        one_stat_teams.append(teams_list[i][stat])
    print(one_stat_teams)
    stand_dev = statistics.stdev(one_stat_teams)
    return stand_dev



def bas_adv_z(stat, mean, stand_dev):

    # calculate and return the z score - > (recorded stat - mean) / standard deviation
    return (stat - mean)/stand_dev
