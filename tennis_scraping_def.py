from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd

## convert url to soup
def soup(url):
    page = urlr.urlopen(url)
    return(BeautifulSoup(page.read(), 'lxml'))

## generate player-year url
def py_url(player_name, gender, year):
    base_url = 'http://www.tennisbetsite.com/players/'
    tour = 'atp/' if gender == 'm' else 'wta/'
    return(base_url + tour + player_name + '.html?year=' + str(year))

## get career reference data for player and year range
def p_ref(player_name, gender, yr_start, yr_end):
    match_df = pd.DataFrame(columns = ['date', 'opponent_id', 'match_url'])
    for y in range(yr_end, yr_start-1, -1):
        r = len(match_df)
        py_soup = soup(py_url(player_name, gender, y))
        res = py_soup.find( 'table', {'class': 'results'} )
        links = [tr.findAll('a') for tr in res.findAll('tr')]
        links = [x for x in links if x != []]
        dates = [tr.findAll('td', {'class': 'date'}) for tr in res.findAll('tr')]
        dates = [x for x in dates if x != []]
        for i in range(len(dates)):
            refs = [x.get('href') for x in links[i]]         
            ref_player = [p for p in refs if 'playerinfo' in p]
            ref_match = [m for m in refs if 'gameinfo' in m]
            ref_player = ref_player[0] if len(ref_player) > 0 else ''
            ref_match = ref_match[0] if len(ref_match) > 0 else ''  
            match_df.loc[r+i] = [dates[i][0].get_text(), 
                         ref_player[55:][:-24], ref_match]
    match_df['m_no'] = list(range(len(match_df)))
    return(match_df)

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
    
## get player match history
def player_history(player_name, gender, yr_start, yr_end):
    player_df = get_player_df()
    ref_table = p_ref(player_name, gender, yr_start, yr_end)
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

## save player history as csv
def player_csv(player_name, gender, yr_start, yr_end):
    phist = player_history(player_name, gender, yr_start, yr_end)
    phist.drop('match_url', axis=1, inplace=True)
    tour = 'atp-' if gender == 'm' else 'wta-'
    base_path = 'C:\\Projects\\tennis-modelling\\data\\player-csvs\\'
    phist.to_csv(base_path + tour + player_name + '.csv')
