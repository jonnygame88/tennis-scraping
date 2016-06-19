from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd
from tennis_scraping_def import *

## get reference data
gender, yr1, yr2 = 'm', 2006, 2016
data_path = 'C:\\Projects\\tennis-modelling\\data\\player-csvs\\'
ids_csv = 'atp-opponent-ids.csv' if gender == 'm' else 'wta-opponent-ids.csv'
player_ids = pd.read_csv(data_path + ids_csv).player_id

errors, start_id, end_id = [], 0, 9
ref_main = pd.DataFrame(columns = ['m_no', 'player_id', 'opponent_id', 
'date', 'round', 'won', 'completed', 'sets', 'match_url', 'event_url'])

for i in range(start_id, end_id+1):
    p_id = int(player_ids[i])
    print(str(i) + ' ' + str(p_id))
    try:
        p_ref = player_ref_data(p_id, gender, yr1, yr2)
        r = len(ref_main)
        for j in range(len(p_ref)):
            ref_main.loc[r+j] = p_ref.loc[j]        
    except Exception:
        errors.append(p_id)
        pass

print('i = ' + str(i) + '\n' + str(len(errors)) + ' error(s): ', errors)
tour_ext = 'atp-ref-' if gender == 'm' else 'wta-ref-'
ref_main.to_csv(data_path + tour_ext + str(start_id) + '-' + str(end_id) + '.csv',
                index = False)
