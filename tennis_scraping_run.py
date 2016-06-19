import pandas as pd
from tennis_scraping_def import *

gender, yr1, yr2 = 'm', 2006, 2016
data_path = 'C:\\Projects\\tennis-modelling\\data\\player-csvs\\'
ids_csv = 'atp-opponent-ids.csv' if gender == 'm' else 'wta-opponent-ids.csv'
player_ids = pd.read_csv(data_path + ids_csv).player_id

start_id, end_id, errors = 0, 99, []
ref_main = pd.DataFrame(columns = ['m_no', 'player_id', 'opponent_id', 
'date', 'won', 'completed', 'sets', 'match_url', 'event_url'])

for i in range(start_id, end_id+1):
    p_id = int(player_ids[i])
    print(str(i) + ' ' + str(p_id))
    try:
        p_ref = player_ref_data(p_id, gender, yr1, yr2)
        r = len(ref_main)
        for i in range(len(p_ref)):
            ref_main.loc[r+i] = p_ref.loc[i]        
    except Exception:
        errors.append(p_id)
        pass

print(str(len(errors)) + ' error(s): ', errors)
ref_main.to_csv(data_path + 'atp-ref-' + str(start_id) + '-' + str(end_id) + '.csv')
# 4373, 6101, 1264
