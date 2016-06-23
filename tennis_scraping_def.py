from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd

## convert url to soup
def soup(url):
    page = urlr.urlopen(url)
    return(BeautifulSoup(page.read(), 'lxml'))

## get career reference data for player and year range
def player_ref_data(player_id, gender, yr_start, yr_end):
    # get starting soup
    base_url = 'http://www.tennisbetsite.com/index.php?option=com_mvx_trdb&'
    ext = '&association=A&Itemid=29' if gender == 'm' else '&association=W&Itemid=29'
    player_url = base_url + 'type=playerinfo&playerid=' + str(player_id) + ext
    player_soup = soup(player_url)
    # get player year urls
    hist = player_soup.find('td', {'class': 'player-history'})
    yr_range = [str(y) for y in range(yr_start, yr_end+1)]
    yrs = [tr.findAll('a') for tr in hist.findAll('tr')]
    yr_links = [y[0].get('href') for y in yrs if y != []]
    yr_vals = [y[0].text for y in yrs if y != []]
    yr_links = [yr_links[i] for i in range(len(yr_vals)) if yr_vals[i] in yr_range]
    # create empty data frame
    player_df = pd.DataFrame(columns = 
    ['m_no', 'player_id', 'opponent_id', 'date', 'round', 
    'won', 'completed', 'sets', 'match_url', 'event_url'])
    # get reference data for each year
    for yr_url in yr_links:
        print(str(player_id) + ' ' + yr_url[-4:])
        # get results table and results rows
        yr_soup = soup('http://www.tennisbetsite.com/' + yr_url)
        res = yr_soup.find('table', {'class': 'results'})
        res_rows = res.findAll('tr')
        links = [tr.findAll('a') for tr in res_rows]
        res_rows = [res_rows[i] for i in range(len(links)) if links[i] != []]
        # get all urls
        links = [tr.findAll('a') for tr in res_rows]
        links = [[x.get('href') for x in l] for l in links]
        # get opponent ids
        opp_ids = [[p for p in l if 'playerid' in p] for l in links]
        opp_ids = [p[0] if p != [] else 'playerid=0&' for p in opp_ids]
        opp_ids = [p[p.find('playerid='):] for p in opp_ids]
        opp_ids = [p[9:p.find('&')] for p in opp_ids]
        # get match urls    
        match_urls = [[m for m in l if 'gameinfo' in m] for l in links]
        match_urls = [m[0][59:] if m != [] else '' for m in match_urls]
        # get tournament urls    
        event_urls = [[e for e in l if 'tournaments' in e] for l in links]
        for i in range(1, len(event_urls)):
            if event_urls[i] == []: event_urls[i] = event_urls[i-1]
        event_urls = [e[0][41:-5] if e != [] else '' for e in event_urls]
        # get winner
        winners = [tr.findAll('td', {'class': 'first'}) for tr in res_rows] 
        ref_win = [int(x[0].findAll('a') == []) for x in winners]
        # get completion statuses
        completed = [tr.findAll('td', {'class': 'cancelled'}) for tr in res_rows]
        completed = [int(x == []) for x in completed]
        # get match dates
        dates = [tr.findAll('td', {'class': 'date'}) for tr in res_rows]
        dates = [d[0].text for d in dates]
        # get tournament rounds
        rounds = [tr.findAll('td', {'class': 'round'}) for tr in res_rows]
        rounds = [r[0].text for r in rounds]
        # get match set scores
        sets = [tr.findAll('td', {'class': 'sets'}) for tr in res_rows]
        sets = [[', '.join([x.text for x in s])] for s in sets]
        # append to player data frame
        r = len(player_df)
        for i in range(len(opp_ids)):
            player_df.loc[r+i] = ['m'+str(r+i), player_id, opp_ids[i], dates[i], 
                          rounds[i], ref_win[i], completed[i], sets[i][0], 
                          match_urls[i], event_urls[i]]
    return(player_df)

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
def get_stats_df():
    return(pd.DataFrame(columns = 
    ['m_no', 'daymonth', 'tournament', 'surface', 'round', 
     'player1', 'nat1', 'player2', 'nat2', 'set1', 'set2', 'set3', 'set4', 'set5',
     'p1_s1perc', 'p2_s1perc', 'p1_aces', 'p2_aces', 'p1_dfs', 'p2_dfs',
     'p1_ues', 'p2_ues', 'p1_s1win', 'p2_s1win', 'p1_s2win', 'p2_s2win',
     'p1_winners', 'p2_winners', 'p1_rwin', 'p2_rwin', 'p1_bpconv', 'p2_bpconv',
     'p1_nas', 'p2_nas', 'p1_tpwin', 'p2_tpwin', 'p1_smax', 'p2_smax',
     'p1_s1avg', 'p2_s1avg', 'p1_s2avg', 'p2_s2avg']))
    
## get player match history
def player_history(player_id, gender, yr_start, yr_end):
    stats_df = get_stats_df()
    ref_table = player_ref_data(player_id, gender, yr_start, yr_end)
    match_urls = ref_table.match_url
    n = len(match_urls)
    for i in range(n):
        print(str(i) + ' / ' + str(n))
        if match_urls[i] != '': 
            m_soup = soup(match_urls[i])
            output = [['m' + str(i)] + match_info(m_soup) + match_stats(m_soup)][0]
        else: 
            output = ['m' + str(i)] + 13*['']
        if len(output) == 42: 
            stats_df.loc[i] = output
        else: 
            stats_df.loc[i] = output[:14] + 28*['']
    return(pd.merge(ref_table, stats_df, on = 'm_no'))

## get player name from player id
def get_name(player_id, gender):
    url0 = 'http://www.tennisbetsite.com/index.php?'
    url1 = 'option=com_mvx_trdb&type=playerinfo&playerid='
    url2 = '&association=A' if gender == 'm' else '&association=W'
    s = soup(url0 + url1 + str(player_id) + url2 + '&Itemid=29')
    return(s.findAll('h1')[1].text.replace(' ', '-').lower())
