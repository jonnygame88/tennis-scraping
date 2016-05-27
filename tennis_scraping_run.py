from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd
pd.set_option('display.width', 1000)
from tennis_scraping_functions import soup, pyr_url, match_urls
from tennis_scraping_functions import match_info, match_stats

## process summary
# initialise (empty) match data table
# get match urls for player 1
# add new opponents to player list
# for each match url: create soup > get info, stats > format, append data
# repeat for player n

## example
player_df = pd.DataFrame(columns = 
['year', 'daymonth', 'tournament',  'surface', 'round', 
'player1', 'nat1', 'player2', 'nat2', 'set1', 'set2', 'set3', 'set4', 'set5',
'p1_s1perc', 'p2_s1perc', 'p1_aces', 'p2_aces', 'p1_dfs', 'p2_dfs',
'p1_ues', 'p2_ues', 'p1_s1win', 'p2_s1win', 'p1_s2win', 'p2_s2win',
'p1_winners', 'p2_winners', 'p1_rwin', 'p2_rwin', 'p1_bpconv', 'p2_bpconv',
'p1_nas', 'p2_nas', 'p1_twin', 'p2_twin', 'p1_smax', 'p2_smax',
'p1_s1avg', 'p2_s1avg', 'p1_s2avg', 'p2_s2avg'])

sample_player, year_start, year_end = 'luis-david-martinez', 2015, 2016
year_range = range(year_end, year_start-1, -1)

for yr in year_range:
    url1 = pyr_url(sample_player, yr)
    soup1 = soup(url1)
    match_links = match_urls(soup1)
    for n in range(len(match_links)):
        r = player_df.shape[0]
        url_match = match_links[n]
        page_match = urlr.urlopen(url_match)
        s = BeautifulSoup(page_match.read(), "lxml")
        output = [str(yr)] + match_info(s) + match_stats(s)
        if len(output) != 42:
            player_df.loc[r+n] = output[:14] + 28*[""]
        else:
            player_df.loc[r+n] = output
        print(n, output[:14])
