# League Information
from sleeper_wrapper import League
import json

league = League(925490163113934848)
league_info = league.get_league()

with open('data/league_info.json', 'w') as f:
    json.dump(league_info, f)