from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd
from tennis_scraping_def import *

## get match stats
match_file = 'atp-match-urls.csv'
data_path = 'C:\\Projects\\tennis-modelling\\data\\reference-csvs\\'
match_urls = pd.read_csv(data_path + match_file)
match_urls = match_urls[match_urls.level != 'Futures']
match_urls = [m for m in match_urls.match_url]

def create_match_csv(a, b):
    match_df = get_stats_df()
    errors = pd.DataFrame(columns = ['err_index', 'err_url'])
    for i in range(a, b+1):
        m = match_urls[i]
        print(str(i))
        try:
            match_df.loc[i] = match_summary(m)
        except Exception:
            errors.loc[i] = [i, m]
            pass
    id_ext = str(a) + '-' + str(b) + '.csv'
    match_df.to_csv(data_path + 'atp-matches-' + id_ext, index = False)
    if len(errors) > 0:
        err0 = pd.read_csv(data_path + 'errors.csv')
        err1 = err0.append(errors)
        err1.to_csv(data_path + 'errors.csv', index = False)

for n in range(13):
    create_match_csv(1000*n, 1000*(n+1)-1)

'''
## get tournament info
events_file = 'atp-event-urls.csv'
data_path = 'C:\\Projects\\tennis-modelling\\data\\reference-csvs\\'
event_urls = pd.read_csv(data_path + events_file).event_url
event_df = pd.DataFrame(columns = ['event_url', 'date', 'level', 'surface', 'prize'])
errors = pd.DataFrame(columns = ['err_index', 'err_url'])

for i in range(len(event_urls)):
    event_i = event_urls[i]
    print(str(i) + ': ' + event_i)
    try:
        event_df.loc[i] = [event_i] + event_summary(event_i)
    except Exception:
        print('error')
        errors.loc[i] = [i, event_i]
        pass  
'''

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
    id_ext = str(start_id) + '-' + str(end_id) + ',csv'
    ref_main.to_csv(data_path + tour_ext + id_ext, index = False)
    if len(errors) > 0:
        err0 = pd.read_csv(data_path + 'errors.csv')
        err1 = err0.append(errors)
        err1.to_csv(data_path + 'errors.csv', index = False)
'''
