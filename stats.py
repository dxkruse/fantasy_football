from sleeper_wrapper import Stats
import pandas as pd
import json
import os

def load_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# Get all stats for a given season
def get_season_stats(type, season):
    stats = Stats()
    stats_info = stats.get_all_stats(type, season)
    return stats_info

# Save all stats for a given season to a JSON file
def save_to_json(data, filename=str):
    if os.path.exists(f'data/{filename}'):
        os.remove(f'data/{filename}')
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f)

# Save all stats for a range of seasons to a JSON file
def save_all_reg_stats(start=str, end=str):
    start = int(start)
    end = int(end)
    stats = get_all_reg_stats(start, end)
    save_to_json(stats, f'{start}_{end}_regular.json')
    print(f'Saved {start}-{end} regular season stats to JSON file')
    return stats
    
# Get all stats for a range of seasons
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

# Sort the raw stats by player_id and year       
def sort_by_player_id(filename=str):
    stats = load_from_json(filename)
    # with open(f'data/player_ids.json', 'r') as f:
    #     player_ids = json.load(f)
              
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

    save_to_json(sorted_data, 'sorted_stats.json')

# Parse position info for a given position and save to JSON file
def parse_pos_info(filename=str, pos=['QB', 'RB', 'WR', 'TE']):
    pos_info_json = load_from_json(filename)
    pos_info = { x: y for x, y in pos_info_json.items()
                if 'position' in y 
                and y['position'] == pos
                }
    save_to_json(pos_info, f'{pos}_info.json')
    return pos_info

# Parse stats from {pos}_info.json for a given position and save to JSON file
def parse_pos_stats(filename=str, pos=['QB', 'RB', 'WR', 'TE']):
    # If player_id in pos_info, add stats to new_data
    pos_info = load_from_json(f'data/{pos}_info.json')
    stats_dict = load_from_json(filename)
    new_data = { 
        year: { 
            player_id: player_stats
            for player_id, player_stats in players.items()
            if player_id in pos_info
        }
        for year, players in stats_dict.items()
    } 
    # save_to_json(new_data, f'{pos}_stats.json')
    return new_data

# Remove players with no stats
def remove_players_no_stats(stats_dict=dict):
    for year in list(stats_dict.keys()):
        for player in list(stats_dict[year].keys()):
            if 'pts_ppr' not in stats_dict[year][player].keys():
                # print(stats_dict[year][player])
                del stats_dict[year][player]
                print(f'Removed {player} {year}')
    return stats_dict

# Calculate fantasy points for a given set of stats
def calculate_fpts(stats_dict=dict):
    scoring_settings = load_from_json('data/scoring_settings.json')
    points = 0
    for player_id, years in stats_dict.items():
        for year, statistics in years.items():
            for stat, value in statistics.items():
                if stat in scoring_settings.keys():
                    # print(stat, value, scoring_settings[stat])
                    points += value * scoring_settings[stat]
                    # print(points)
            statistics['calculated_fpts'] = points
            # print(points)
            points = 0
    return stats_dict
                
def flatten_stats(filename=str):
    stats_dict = load_from_json(filename)
    new_dict = {}
    for year in stats_dict.keys():
        # print(year)
        for statistics in stats_dict[year].items():
            statistics[1]['year'] = year
            statistics[1]['player_id'] = statistics[0]      
            new_dict[len(new_dict) + 1] = statistics[1]
    return new_dict

# Replace NaN with { 'stats': 0 } and convert dicts to dataframes  
def replace_nan_convert_dicts(dfStats=pd.DataFrame):
    for col in dfStats.columns:
        for row in dfStats.index:        
            # print(dfStats[col][row])
            if isinstance(dfStats[col][row], dict):
                dfStats[col][row] = pd.DataFrame.from_dict(dfStats[col][row], orient='index')
            elif isinstance(dfStats[col][row], float):
                dfStats[col][row] = pd.DataFrame({ 'stats': 0 }, index=[0]).transpose()
    return dfStats

# stats_dict = load_from_json('data/2021_2022_regular.json')
# pos_info = parse_pos_info('data/players_info.json', 'QB')
# print(pos_info)


# flatten_stats('data/2021_regular.json')
#save_all_reg_stats(2009, 2022)
#sort_by_player_id('data/2009_2022_regular.json')
# get_all_reg_stats(2019, 2020)
# earliest_season = get_season_stats('regular', '2009')
# save_stats_to_json(earliest_season, 'earliest_season')
# parse_pos_stats('data/QB_info.json')


