# League Information
from sleeper_wrapper import League
import json
import os


def get_league_info():
    league = League(925490163113934848)
    league_info = league.get_league()
    return league_info

def get_scoring_settings():
    league_info = load_from_json('data/league_info.json')
    scoring_settings = league_info['scoring_settings']
    save_to_json(scoring_settings, 'scoring_settings.json')    

def load_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def save_to_json(data, filename=str):
    if os.path.exists(f'data/{filename}'):
        os.remove(f'data/{filename}')
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f)
        
# get_scoring_settings()
