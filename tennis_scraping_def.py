from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd

## convert url to soup
def soup(url):
    page = urlr.urlopen(url)
    return(BeautifulSoup(page.read(), 'lxml'))
    
## get tour list for year
def tour_csv(year):
    tour_df = pd.DataFrame(columns = 
    ['tourn_year', 'tourn_mday', 'tourn_name', 'tourn_assoc',
    'tourn_surface', 'tourn_country', 'tourn_rank', 'tourn_code'])
    base_url = 'http://www.tennisbetsite.com/index.php'
    ext_url = '?option=com_mvx_trdb&Itemid=29&limit=10000&limitstart=0&q='
    url_year = base_url + ext_url + str(year) + '&type=tourslist'
    soup_year = soup(url_year)
    tourn_list = soup_year.find( 'table', {'class': 'tours'} )
    yrs = [tr.findAll('td', {'class': 'year'}) for tr in tourn_list.findAll('tr')]
    yrs = [x[0].text for x in yrs[1:]]
    dates = [tr.findAll('td', {'class': 'date'}) for tr in tourn_list.findAll('tr')]
    dates = [x[0].text for x in dates[1:]]
    tourns = [tr.findAll('td', {'class': 'tours'}) for tr in tourn_list.findAll('tr')]
    tourns = [x[0].text for x in tourns[1:]]
    assoc = [tr.findAll('td', {'class': 'assoc'}) for tr in tourn_list.findAll('tr')]
    assoc = [x[0].text for x in assoc[1:]]
    surfaces = [tr.findAll('td', {'class': 'surf'}) for tr in tourn_list.findAll('tr')]
    surfaces = [x[0].text for x in surfaces[1:]]
    countries = [tr.findAll('td', {'class': 'country'}) for tr in tourn_list.findAll('tr')]
    countries = [x[0].text for x in countries[1:]]
    ranks = [tr.findAll('td', {'class': 'rank'}) for tr in tourn_list.findAll('tr')]
    ranks = [x[0].text for x in ranks[1:]]
    links = [tr.findAll('a') for tr in tourn_list.findAll('tr')]
    links = [x[0].get('href') for x in links[1:]]
    for i in range(len(dates)): 
        tour_df.loc[i] = [yrs[i], dates[i], tourns[i], assoc[i],
                    surfaces[i], countries[i], ranks[i], links[i][41:][:-5]]
    base_path = 'C:\\Projects\\tennis-modelling\\data\\tennis-bet-site\\'
    tour_df.to_csv(base_path + 'tour-list-' + str(year) + '.csv')

## get match info from match soup
def match_info(match_soup):
    tourn = match_soup.h2.get_text()
    surface = match_soup.findAll('span', attrs = {'class': 'maininfo'})[0].get_text()
    surface = surface[0:surface.find(',')]
    date = match_soup.findAll('div', attrs = {'class': 'calendar'})[0].get_text()
    date = date.replace('\n', ' ').replace(' ', '')
    soup_scores = match_soup.findAll('table', attrs = {'class': 'scores'})[0]
    round = soup_scores.findAll('td', attrs = {'class': 'round'})[0].get_text()
    players = [x.get_text() for x in soup_scores.findAll('acronym', {'title': True})]
    sets = [x.get_text() for x in soup_scores.findAll('td', attrs = {'class': 'set'})]
    return([date, tourn, surface, round] + players + sets)

## get match stats from match soup
def match_stats(match_soup):
    gs = match_soup.findAll('table', attrs = {'class': 'gamestats'})[0].tbody
    if gs is None:
        return([])
    else:
        return([x.get_text() for x in gs.findAll(attrs = {'class': 'value'})])

## generate empty data frame
def get_player_df():
    return(pd.DataFrame(columns = 
    ['m_no', 'ref_player', 'daymonth', 'tournament',  'surface', 'round', 
     'player1', 'nat1', 'player2', 'nat2', 'set1', 'set2', 'set3', 'set4', 'set5',
     'p1_s1perc', 'p2_s1perc', 'p1_aces', 'p2_aces', 'p1_dfs', 'p2_dfs',
     'p1_ues', 'p2_ues', 'p1_s1win', 'p2_s1win', 'p1_s2win', 'p2_s2win',
     'p1_winners', 'p2_winners', 'p1_rwin', 'p2_rwin', 'p1_bpconv', 'p2_bpconv',
     'p1_nas', 'p2_nas', 'p1_twin', 'p2_twin', 'p1_smax', 'p2_smax',
     'p1_s1avg', 'p2_s1avg', 'p1_s2avg', 'p2_s2avg']))

## get player name from player id
def get_name(player_id, gender):
    url1 = 'http://www.tennisbetsite.com/index.php?option=com_mvx_trdb&type=playerinfo&playerid=' 
    url2 = '&association=A&Itemid=29/' if gender == 'm' else '&association=W&Itemid=29'
    s = soup(url1 + str(player_id) + url2)
    return(s.findAll('h1')[1].text.replace(' ', '-').lower())
