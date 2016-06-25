from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd
from tennis_scraping_def import *

## get tournament info
data_path = 'C:\\Projects\\tennis-modelling\\data\\reference-csvs\\'
tour_ext = 'atp-event-urls.csv'
event_urls = pd.read_csv(data_path + tour_ext).event_url

for i in [1, 10, 100, 500, 1000, 5000]:
    print(event_urls[i], '\n', event_summary(event_urls[i]), '\n\n')

'''
## get reference data
gender, yr1, yr2 = 'm', 2006, 2016
data_path = 'C:\\Projects\\tennis-modelling\\data\\reference-csvs\\'
tour_ext = 'atp-ref-' if gender == 'm' else 'wta-ref-'
ids_csv = 'atp-opponent-ids.csv' if gender == 'm' else 'wta-opponent-ids.csv'
player_ids = pd.read_csv(data_path + ids_csv).player_id

def create_ref_csv(start_id, end_id):
    ref_main = pd.DataFrame(columns = 
    ['m_no', 'player_id', 'opponent_id', 'date', 'round', 
    'won', 'completed', 'sets', 'match_url', 'event_url'])
    errors = pd.DataFrame(columns = ['err_index', 'err_id'])
    for i in range(start_id, end_id+1):
        p_id = int(player_ids[i])
        print(str(i) + ': ' + str(p_id))
        try:
            p_ref = player_ref_data(p_id, gender, yr1, yr2)
            r = len(ref_main)
            for j in range(len(p_ref)):
                ref_main.loc[r+j] = p_ref.loc[j]        
        except Exception:
            errors.loc[i] = [i, p_id]
            pass
    id_ext = str(start_id) + '-' + str(end_id)
    ref_main.to_csv(data_path + tour_ext + id_ext + '.csv', index = False)
    if len(errors) > 0:
        errors.to_csv(data_path + 'errors-' + id_ext + '.csv', index = False)
'''