from pprint import pprint
import datetime
import requests
from bs4 import BeautifulSoup

### MLB ANALYSIS ###

import mlbgame



# Get 10 years of data!

def get_mlb_data():
    data_years = [datetime.date(2005 + n, 9, 25) for n in range(0,10)]

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

def get_nhl_data():
    years = [str(year) for year in range(2005, 2016)]
    for year in years: 
        html = requests.get("https://www.nhl.com/standings/" + year).content.decode('utf-8','ignore') 
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.findAll("div"))

get_nhl_data()