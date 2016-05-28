import pandas as pd
from tennis_scraping_def import *
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 250)

player, gender, yr1, yr2 = 'serena-williams', 'w', 2015, 2016
phist = player_history(player, gender, yr1, yr2)
phist.drop('match_url', axis=1, inplace=True)

tour = 'atp-' if gender == 'm' else 'wta-'
base_path = 'C:\\Projects\\tennis-modelling\\data\\player-csvs\\'
# phist.to_csv(base_path + tour + player + '.csv')
