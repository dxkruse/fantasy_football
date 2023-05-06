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
    # print(stats.keys())
    with open(f'data/player_ids.json', 'r') as f:
        player_ids = json.load(f)
    # print(player_ids.keys())
    # print(sorted_stats)
    # print(sorted_stats)
    # sorted_stats = sorted(stats.values(), key=lambda x: int(x.keys()[0]))
    # for id in player_ids.keys():
        # print(id)
        
    # Create a new dictionary with the merged data
    # merged_data = {}
    # for year, players in stats.items():
    #     for player_id, player_stats in players.items():
    #         if player_id not in merged_data:
    #             merged_data[player_id] = {}
    #         if year not in merged_data[player_id]:
    #             merged_data[player_id][year] = player_stats
                
    # Create a new dictionary with the merged data
    merged_data = {}
    for year, players in stats.items():
        for player_id, player_stats in players.items():
            # print(player_ids.get(player_id))
            player_name = player_ids.get(player_id)
            if player_name not in merged_data:
                merged_data[player_name] = {}
            if player_id not in merged_data[player_name]:
                merged_data[player_name][player_id] = {}
            if year not in merged_data[player_name][player_id]:
                merged_data[player_name][player_id][year] = player_stats

    sorted_data = {}
    for player_name, player_ids in merged_data.items():
        sorted_player_ids = dict(sorted(player_ids.items(), key=lambda x: x[0]))
        sorted_data[player_name] = sorted_player_ids
        for player_id, years in sorted_player_ids.items():
            sorted_years = dict(sorted(years.items(), key=lambda x: x[0]))
            sorted_data[player_name][player_id] = sorted_years
    # sorted_data = {}
    # for player_id, years in merged_data.items():
    #     sorted_years = dict(sorted(years.items(), key=lambda x: x[0]))
    #     sorted_data[player_id] = sorted_years
    # sorted_data = dict(sorted(sorted_data.items(), key=lambda x: x[0]))
    
    # final_data = {}
    # for player_id, years in sorted_data.items():
    #     final_data[player_id] = {}
    #     for year, player_stats in years.items():
    #         final_data[player_id][year] = player_stats            

    save_stats_to_json(sorted_data, 'sorted_stats')

def save_all_post_stats(start=str, end=str):
    for season in range(start, end):
        stats = get_season_stats('post', season)            
        save_stats_to_json(stats)
        print(f'Saved {season[0]}-{season[-1]} post season stats to JSON file')
        
# save_all_reg_stats(2018, 2022)
sort_by_player_id('data/2018_2022_regular.json')
#get_all_reg_stats(2019, 2020)

