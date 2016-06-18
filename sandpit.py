from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd
from tennis_scraping_def import *
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 250)

## process
# player_id list from tour_list
# year links from player_id page
# opponent_id, won, sets, date, tournament_link (repeated)
# match_url and match_data
# tour_level, prize_money from tournament_link

base_url = 'http://www.tennisbetsite.com/index.php?option=com_mvx_trdb&'
atp_ext = '&association=A&Itemid=29'

player_id = 1075
player_url = base_url + 'type=playerinfo&playerid=' + str(player_id) + atp_ext
s = soup(player_url)

hist = s.find('td', {'class': 'player-history'})
yr_range = [str(y) for y in range(2006, 2017)]
yrs = [tr.findAll('a') for tr in hist.findAll('tr')]
yr_links = [y[0].get('href') for y in yrs if y != []]
yr_vals = [y[0].text for y in yrs if y != []]
yr_links = [yr_links[i] for i in range(len(yr_vals)) if yr_vals[i] in yr_range]

res = s.find('table', {'class': 'results'})
res_rows = res.findAll('tr')
links = [tr.findAll('a') for tr in res_rows]
res_rows = [res_rows[i] for i in range(len(links)) if links[i] != []]

links = [tr.findAll('a') for tr in res_rows]
links = [[x.get('href') for x in l] for l in links]

opp_ids = [[p for p in l if 'playerid' in p] for l in links]
opp_ids = [p[0][55:] if p != [] else '-1' for p in opp_ids]

match_urls = [[m for m in l if 'gameinfo' in m] for l in links]
match_urls = [m[0] if m != [] else 'x' for m in match_urls]

event_urls = [[e for e in l if 'tournaments' in e] for l in links]
for i in range(1, len(event_urls)):
    if event_urls[i] == []: event_urls[i] = event_urls[i-1]
event_urls = [e[0] if e != [] else 'x' for e in event_urls]

dates = [tr.findAll('td', {'class': 'date'}) for tr in res_rows]
dates = [d[0].text for d in dates]
sets = [tr.findAll('td', {'class': 'sets'}) for tr in res_rows]
sets = [[', '.join([x.text for x in s])] for s in sets]
