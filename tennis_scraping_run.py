import pandas as pd
from tennis_scraping_def import *
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 250)

data_path = 'C:\\Projects\\tennis-modelling\\data\\player-csvs\\'
opponent_ids = pd.read_csv(data_path + 'opponent-ids-atp.csv').opponent_id
completed, to_complete = 2, 10
gender, yr1, yr2 = 'm', 2006, 2016

for i in list(range(completed, to_complete)):
    player_name = get_name(opponent_ids[i], gender)
    try:
        print(player_name)
        player_csv(player_name, gender, yr1, yr2)
    except Exception:
        try:
            print(player_name + str('-2'))
            player_csv(player_name + str('-2'), gender, yr1, yr2)
        except Exception:
            pass

## test: jimmy wang, john isner
