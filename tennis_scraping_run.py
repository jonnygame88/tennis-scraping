from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 250)

from tennis_scraping_def import soup, py_url, p_ref, get_player_df
from tennis_scraping_def import match_info, match_stats

def f(player_name, yr_start, yr_end):
    player_df = get_player_df()
    ref_table = p_ref(player_name, yr_start, yr_end)
    match_urls = ref_table.match_url
    n = len(match_urls)
    for i in range(n):
        print(str(i) + ' / ' + str(n))
        if match_urls[i] != '': 
            m_soup = soup(match_urls[i])
            output = [[str(i), player_name] + 
            match_info(m_soup) + match_stats(m_soup)][0]
        else: output = [str(i)] + 14*['']
        if len(output) == 43: player_df.loc[i] = output
        else: player_df.loc[i] = output[:15] + 28*['']
    ref_table['m_no'] = ['m' + str(k) for k in ref_table.m_no]
    player_df['m_no'] = ['m' + str(k) for k in player_df.m_no]
    return(pd.merge(ref_table, player_df, on = 'm_no'))

h = f('andy-murray', 2015, 2016)
h.drop('match_url', axis=1, inplace=True)
player_name, yr_start, yr_end = 'andy-murray', 2015, 2016

h.to_csv('C:\\Projects\\tennis-modelling\\data\\andy-murray.csv')

## add new opponents to player list
## for each match url: create soup > get info, stats > format, append data
## ref_player[55:][:-24], ref_match[83:][:-14]
