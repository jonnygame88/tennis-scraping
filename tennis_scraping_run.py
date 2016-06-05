import pandas as pd
from tennis_scraping_def import *
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 250)

data_path = 'C:\\Projects\\tennis-modelling\\data\\player-csvs\\'
opponent_ids = pd.read_csv(data_path + 'opponent-ids-atp.csv').opponent_id
start_loc, end_loc = 11, 15
gender, yr1, yr2 = 'm', 2006, 2016
errors = []

for i in list(range(start_loc, end_loc+1)):
    player_name = get_name(opponent_ids[i], gender)
    try:
        print(i, player_name)
        player_csv(player_name, gender, yr1, yr2)
    except Exception:
        try:
            print(i, player_name + str('-2'))
            player_csv(player_name + str('-2'), gender, yr1, yr2)
        except Exception:
            errors.append(player_name)
            pass

print(str(len(errors)) + ' error(s): ', errors)
