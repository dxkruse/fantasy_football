from sleeper_wrapper import Players
import json
# Save Player IDs to JSON file

def get_player_info():
    players = Players()
    players_info = players.get_all_players()
    return players_info    

def get_player_ids():
    players = Players()
    players_info = players.get_all_players()
    player_ids = {}
    for i in players_info.keys():
        player_name = players_info[i]['first_name'] + ' ' + players_info[i]['last_name']
        player_ids[i] = player_name
    return player_ids

def save_to_json(data):
    filename = [var_name for var_name in globals() if globals()[var_name] == data][0]
    with open(f'data/{filename}.json', 'w') as f:
        json.dump(data, f)
      
def load_from_json(filename):
    with open(f'data/{filename}.json', 'r') as f:
        data = json.load(f)
    return data






