from sleeper_wrapper import Players
from players import *
from stats import *
import pandas as pd

players = Players()
players.get_all_players()

import players
import stats
import pandas as pd

data = pd.DataFrame(stats.load_from_json('data/sorted_stats.json'))
data.head()
