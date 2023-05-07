from sleeper_wrapper import Stats
import pandas as pd
import json

def load_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def load_from_json2(filename):
    with open(f'data/{filename}.json', 'r') as f:
        data = json.load(f)
    return data

def get_season_stats(type, season):
    stats = Stats()
    stats_info = stats.get_all_stats(type, season)
    return stats_info

def save_stats_to_json(data, filename=str):
    with open(f'data/{filename}.json', 'w') as f:
        json.dump(data, f)

def save_all_reg_stats(start=str, end=str):
    start = int(start)
    end = int(end)
    stats = get_all_reg_stats(start, end)     
    with open(f'data/{start}_{end}_regular.json', 'w') as f:
        json.dump(stats, f)
    print(f'Saved {start}-{end} regular season stats to JSON file')   

def get_all_reg_stats(start=str, end=str):
    start = int(start)
    end = int(end)
    stats = {}   
    for season in range(start, end+1):
        season = str(season)
        stats_temp = get_season_stats('regular', season)
        stats = stats | {season : stats_temp}
    print(stats.keys())
    return stats
        
def sort_by_player_id(filename=str):
    stats = load_from_json(filename)
    with open(f'data/player_ids.json', 'r') as f:
        player_ids = json.load(f)
              
    # Create a new dictionary with the merged data
    merged_data = {}
    for year, players in stats.items():
        for player_id, player_stats in players.items():
            if player_id not in merged_data:
                merged_data[player_id] = {}
            if year not in merged_data[player_id]:
                merged_data[player_id][year] = player_stats
                
    # Sort the data by player_id and year
    sorted_data = {}
    for player_id, years in merged_data.items():
        sorted_years = dict(sorted(years.items(), key=lambda x: x[0]))
        sorted_data[player_id] = sorted_years
    sorted_data = dict(sorted(sorted_data.items(), key=lambda x: x[0]))
    
    final_data = {}
    for player_id, years in sorted_data.items():
        final_data[player_id] = {}
        for year, player_stats in years.items():
            final_data[player_id][year] = player_stats            

    save_stats_to_json(sorted_data, 'sorted_stats')

def parse_pos_ids(filename=str, pos=['QB', 'RB', 'WR', 'TE']):
    pos_info_json = load_from_json(filename)
    pos_info = { x: y for x, y in pos_info_json.items()
                if 'position' in y 
                and y['position'] == pos
                }
    save_stats_to_json(pos_info, f'{pos}_info')
    return pos_info
    
def parse_pos_stats(filename=str):
    pos_stats = load_from_json(filename)
    new_data = { x: y for x, y in pos_stats.items()
                if 'position' in y 
                and y['position'] == pos
                }
    save_stats_to_json(new_data, f'{pos}_stats')
    
    
        
#save_all_reg_stats(2009, 2022)
#sort_by_player_id('data/2009_2022_regular.json')
# get_all_reg_stats(2019, 2020)
# earliest_season = get_season_stats('regular', '2009')
# save_stats_to_json(earliest_season, 'earliest_season')
parse_pos_ids('data/players_info.json', 'QB')


