from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd

## convert url to soup
def soup(url):
    page = urlr.urlopen(url)
    return(BeautifulSoup(page.read(), "lxml"))

## get player-year url
def pyr_url(player_name, year):
    base_url = "http://www.tennisbetsite.com/players/atp/"
    return(base_url + player_name + ".html?year=" + str(year))

## get ref data from player-year soup
def match_ref(pyr_soup):
    info = [x.get_text() for x in pyr_soup.findAll('acronym', {"title": True})]
    return([x for x in info if len(x) > 0 and x != 'Surf.'])

## get match urls from player-year soup
def match_urls(pyr_soup):
    match_links = []
    for link in pyr_soup.find_all('a'):
        link_url = link.get('href')
        if "gameinfo" in link_url and link_url not in match_links:
            match_links.append(link_url)
    return(match_links)

## get match info
def match_info(match_soup):
    tourn = match_soup.h2.get_text()
    surface = match_soup.findAll('span', attrs = {'class': 'maininfo'})[0].get_text()
    surface = surface[0:surface.find(',')]
    date = match_soup.findAll('div', attrs = {'class': 'calendar'})[0].get_text()
    date = date.replace('\n', ' ').replace(' ', '')
    soup_scores = match_soup.findAll('table', attrs = {'class': 'scores'})[0]
    round = soup_scores.findAll('td', attrs = {'class': 'round'})[0].get_text()
    players = [x.get_text() for x in soup_scores.findAll('acronym', {"title": True})]
    sets = [x.get_text() for x in soup_scores.findAll('td', attrs = {'class': 'set'})]
    return([date, tourn, surface, round, players, sets])

## get match stats
def match_stats(match_soup):
    gs = match_soup.findAll('table', attrs = {'class': 'gamestats'})[0].tbody
    if gs is None:
        return([])
    else:
        gs_title = gs.findAll(attrs = {'class': 'title'})
        gs_val = gs.findAll(attrs = {'class': 'value'})
        t_metrics = [i.get_text() for i in gs_title]
        t_vals = [i.get_text() for i in gs_val]
        t_entries = [[t_metrics[i], t_vals[2*i], t_vals[2*i + 1]] for i in range(14)]
        return(pd.DataFrame(t_entries, columns = ['metric', 'player1', 'player2']))

## add to player list
# add opponent if opponent not in player list
# f(current_list, new_url)

## format and append match data
# check columns match, append row
# f(current_data, new_row)
