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


# pprint(get_mlb_data())

from bs4 import BeautifulSoup

def get_nhl_data():
    years = [str(year) for year in range(2008, 2016)]
    nhl_data = {}
    for year in years:
        year_data = {}
        html = requests.get("http://www.espn.com/nhl/standings/_/year/{}/seasontype/2".format(year)).content
        soup = BeautifulSoup(html, "lxml")
        table = soup.find('table', {'class': 'tablehead'})
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [elem.text.strip() for elem in cols if len(cols) > 11]
            if cols and cols[9] != "HOME":
                hwins, hlosses, hties = [int(x) for x in cols[9].split('-')]
                awins, alosses, aties = [int(x) for x in cols[10].split('-')]
                team_name = cols[0][4:]
                year_data.update({
                    team_name: {
                        'away_wins': awins,
                        'away_losses': alosses,
                        'away_ties': aties,
                        # Ok so apparently a tie counts as a 1/2 win
                        'away_percent_wins': (awins + aties / 2) / (awins + alosses + aties),
                        'home_wins': hwins,
                        'home_losses': hlosses,
                        'home_ties': hties,
                        'home_percent_wins': (hwins + hties / 2) / (hwins + hlosses + hties),
                        }
                    })
        nhl_data.update({year: year_data})
    return nhl_data

pprint(get_nhl_data())

from nba_py import team, constants

### NBA DATA ###

def get_nba_data():
    years = [year for year in range(2008, 2016)]
    standings = {}
    for year in years:
        year_standings = {}
        for _, team_data in constants.TEAMS.items():
            team_id = team_data['id']
            team_record = {}
            away_score_data = team.TeamGeneralSplits(team_id, location="Road", season=str(year) + '-' + "%02d" % ((year + 1) % 100)).wins_losses()
            awins, alosses = [x['GP'] for x in away_score_data]
            home_score_data = team.TeamGeneralSplits(team_id, location="Home", season=str(year) + '-' + "%02d" % ((year + 1) % 100)).wins_losses()
            hwins, hlosses = [x['GP'] for x in home_score_data]
            team_record.update({
                team_data['name']: {
                    'away_wins': awins,
                    'away_losses': alosses,
                    'away_percent_wins': awins / (awins + alosses),
                    'home_wins': hwins,
                    'home_losses': hlosses,
                    'home_percent_wins': hwins / (hwins + hlosses),
                }
            })
            year_standings.update(team_record)
        standings.update({str(year): year_standings})
    return standings

# import json
# nba_data = get_nba_data()
# with open('data.json', 'w') as outfile:
#         json.dump(nba_data, outfile)
