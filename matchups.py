from nba_api.stats.endpoints import leaguegamelog, scoreboard
from teams import teams

# using the nba api endpoint leaguegamelog find the previous matchups on a given date and season as well as current games on the schedule
## NOTEEEEEEEEE: date is MM/DD/YYYY and season is YYYY-YY this is a friendly reminder this will give you a stupid error so when it happens again here you go


def current_matchups(date):

    # all games on a date this season
    curr_matchups = scoreboard.Scoreboard(league_id='00', game_date=date)
    curr_matchups_dict = curr_matchups.get_normalized_dict()
    games_list = curr_matchups_dict['GameHeader']

    h_a_dict = {}

    for game in games_list:                         # loop through each game on date
        awayTeamID = game['VISITOR_TEAM_ID']

        for team, team_id in teams.items():  # get name of the away team 
            if team_id == awayTeamID:
                away = team

        home_id = game['HOME_TEAM_ID']

        for team, team_id in teams.items():  # get name of the home team 
            if team_id == home_id:
                home = team

       

        h_a_dict.update({home:away})

    return h_a_dict

print(current_matchups('02/10/2024'))



def past_matchups (date, season):

    prev_matchups = leaguegamelog.LeagueGameLog(season = season, league_id = '00' , season_type_all_star = 'Regular Season', date_from_nullable = date, date_to_nullable = date)

    prev_matchups_dict = prev_matchups.get_normalized_dict()
    teams_list = prev_matchups_dict['LeagueGameLog']

    # create a win loss list and a home away dict
    w_l_list =[]
    h_a_dict = {}
    # the dict is in format of {home:away}

    # the reason we are looping by steps of 2 is because the database stores teams 
    for i in range(0, len(teams_list), 2): 
        # the api stores current teams as away as ATL @ MIN which means atlant is playing in minnesota
        if '@' in teams_list[i]['MATCHUP']:
            away = teams_list[i]['TEAM_NAME']
            home = teams_list[i+1]['TEAM_NAME']
            # append result of game in the perspective of the home team
            w_l_list.append(teams_list[i+1]['WL'])

        
        else:
            away = teams_list[i+1]['TEAM_NAME']
            home = teams_list[i]['TEAM_NAME']
            w_l_list.append(teams_list[i]['WL'])  # append result of game in the perspective of the home team

        h_a_dict.update({home:away})

    result_combined_list = [h_a_dict, w_l_list]

    return result_combined_list

# print(past_matchups('02/10/2024', '2023-24'))