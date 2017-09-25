from pprint import pprint
import datetime
import requests

### MLB DATA ###

import mlbgame


# Get 10 years of data!

def get_mlb_data():
    data_years = [datetime.date(2005 + n, 9, 25) for n in range(0, 10)]

    # This is the main dict which holds data for each year
    standings_by_year = {}

    for year in data_years:
        mlb_teams = []
        for division in mlbgame.info.standings(year)['divisions']:
            for team in division['teams']:
                mlb_teams.append(mlbgame.info.Team(team))

        team_standings = [{
            team.team_short: {
                'away_wins': int(team.away.split('-')[0]),
                'away_losses': int(team.away.split('-')[1]),
                'home_wins': int(team.home.split('-')[0]),
                'home_losses': int(team.home.split('-')[1]),
            }
        } for team in mlb_teams]

        standings_by_year.update({year.year: team_standings})
    return standings_by_year


pprint(get_mlb_data())

# from nhlscrapi.games.game import Game, GameType, GameKey

# def get_nhl_data():
#     years = [year for year in range(2008, 2016)]
#     for year in years:
#         gt = GameType.Regular
#         game_key = GameKey(year, 1226, gt)
#         game = Game(game_key)
#         pprint(game.cum_stats)
# get_nhl_data()

from nba_py import team, constants
import itertools


### NBA DATA ###

def get_nba_data():
    years = [year for year in range(2008, 2016)]
    standings = {}
    for year in years:
        year_standings = {}
        for _, team_data in constants.TEAMS.items():
            team_id = team_data['id']
            team_record = {}
            team_record.update({
                team_data['name']: {
                    x: y for (x, y) in zip(
                        ["away_losses", "away_wins", "home_losses", "home_wins"],
                        itertools.chain(*[
                            [str(x['GP']) for x in team.TeamGeneralSplits(team_id, location=loc, season=str(
                                year) + '-' + "%02d" % ((year + 1) % 100)).wins_losses()[::-1]]
                            for loc in ["Road", "Home"]
                        ])
                    )
                }
            })
            year_standings.update(team_record)
        standings.update({year: year_standings})
    return standings

pprint(get_nba_data())
