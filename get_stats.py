
from teams import teams
from nba_api.stats.endpoints import teamdashboardbygeneralsplits, leaguedashteamstats
import time


def get_team_stats(team, start, end, season = '2023-24'):

    # gathering the specified teams information by calling the applicable function within the API endpoint in this TeamDashboardByGeneralSplits this will 
    # give me acces to the method within the endpoint which can feed me data on per 100possessions already which will be a key factor 
    bas_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id = teams[team], per_mode_detailed= 'Per100Possessions', date_from_nullable = start, date_to_nullable= end, season = season)
    bas_team_dict = bas_team_info.get_normalized_dict()  
    print(bas_team_dict)
    bas_team_dash = bas_team_dict['OverallTeamDashboard'][0] # access specifically the overall dashboard for the teams stats not the other ones as this is the best coverage for data from the api in this case
    # do the same for win percentage stats rebounds turnovers and plus minus
    rebounds = bas_team_dash['REB']
    win_percentage = bas_team_dash['W_PCT']
    
    turnovers = bas_team_dash['TOV']
    plus_minus = bas_team_dash['PLUS_MINUS']
    # these will gather the columns associated with the stats we need

    # possible require another form of stats to run ???? fix later

    adv_team_info = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=teams[team], measure_type_detailed_defense = 'Advanced', date_from_nullable=start, date_to_nullable = end, season=season)
    adv_team_dict = adv_team_info.get_normalized_dict()
    adv_team_dash = adv_team_dict['OverallTeamDashboard'][0]

    # gather more stats specifically Offensive rating and defensive rating by the nba and the true shooting pct

    defensive_rating = adv_team_dash['DEF_RATING']
    offensive_rating = adv_team_dash['OFF_RATING']
    true_shooting_pct = adv_team_dash['TS_PCT']

    # sort these stats into a dictionary for easier handling and reutnr this dictionary

    team_stats= {
        'W_PCT':win_percentage,
        'REB':rebounds,
        'TOV':turnovers,
        'PLUS_MINUS':plus_minus,
        'OFF_RATING':offensive_rating,
        'DEF_RATING': defensive_rating,
        'TS_PCT':true_shooting_pct,
    }
    print(team_stats)
    return team_stats
    # print(adv_team_dict)

print(get_team_stats('Atlanta Hawks', '10/24/2023', '02/11/2024'))

