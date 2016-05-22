## match list: list year urls on player page, get matches for each url
## player list: add opponent if opponent not in player list
## player1 > get match list > format and append match data, add to player list
## repeat for players in player list

from bs4 import BeautifulSoup
import urllib.request as urlr
import datetime
import pandas as pd
pd.set_option('display.width', 1000)

## get match urls
url_player = "http://www.tennisbetsite.com/players/atp/novak-djokovic.html"
page_player = urlr.urlopen(url_player)
soup_player = BeautifulSoup(page_player.read(), "lxml")
match_links = []
for link in soup_player.find_all('a'):
    link_url = link.get('href')
    if "gameinfo" in link_url and link_url not in match_links:
        match_links.append(link_url)

## get match info
def match_info(soup_match):
    tourn = soup_match.h2.get_text()
    surface = soup_match.findAll('span', attrs = {'class': 'maininfo'})[0].get_text()
    surface = surface[0:surface.find(',')]
    date = soup_match.findAll('div', attrs = {'class': 'calendar'})[0].get_text()
    date = date.replace('\n', ' ').replace(' ', '')
    soup_scores = soup_match.findAll('table', attrs = {'class': 'scores'})[0]
    round = soup_scores.findAll('td', attrs = {'class': 'round'})[0].get_text()
    players = [x.get_text() for x in soup_scores.findAll('acronym', {"title": True})]
    sets = [x.get_text() for x in soup_scores.findAll('td', attrs = {'class': 'set'})]
    return([date, tourn, surface, round, players, sets])

## get match stats
def match_stats(soup_match):
    gs = soup_match.findAll('table', attrs = {'class': 'gamestats'})[0].tbody
    if gs is None:
        return([])
    else:
        gs_title = gs.findAll(attrs = {'class': 'title'})
        gs_val = gs.findAll(attrs = {'class': 'value'})
        t_metrics = [i.get_text() for i in gs_title]
        t_vals = [i.get_text() for i in gs_val]
        t_entries = [[t_metrics[i], t_vals[2*i], t_vals[2*i + 1]] for i in range(14)]
        return(pd.DataFrame(t_entries, columns = ['metric', 'player1', 'player2']))

## output
tstart = datetime.datetime.now()
for n in range(len(match_links)):
    url_match = match_links[n]
    page_match = urlr.urlopen(url_match)
    s = BeautifulSoup(page_match.read(), "lxml")
    print(match_info(s), '\n\n', match_stats(s), '\n')
print(len(match_links), tstart, datetime.datetime.now())
