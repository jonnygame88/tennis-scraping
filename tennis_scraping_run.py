from bs4 import BeautifulSoup
import urllib.request as urlr
import datetime
import pandas as pd
pd.set_option('display.width', 1000)
from tennis_scraping_functions import soup, pyr_url, match_ref, match_urls
from tennis_scraping_functions import match_info, match_stats

## process summary
# initialise (empty) match data table
# get match urls for player 1
# add new opponents to player list
# for each match url: create soup > get info, stats > format, append data
# repeat for player n

## example
sample_player, year_start, year_end = 'tomislav-brkic', 2010, 2012
year_range = range(year_start, year_end + 1)

file = open("tennis-sample.txt", "w")
for yr in year_range:
    url1 = pyr_url(sample_player, yr)
    soup1 = soup(url1)
    file.write(url1 + '\n')
    ref1 = match_ref(soup1)
    for i in range(int(len(ref1)/4)):
        file.write(str(ref1[4*i]) + ' ' + str(ref1[4*i+1]) + ' ' +
                   str(ref1[4*i+2]) + ' ' + str(ref1[4*i+3])+'\n')
    match_links = match_urls(soup1)
    file.write('t_start =' + str(datetime.datetime.now()) + '\n')
    for n in range(len(match_links)):
        url_match = match_links[n]
        page_match = urlr.urlopen(url_match)
        s = BeautifulSoup(page_match.read(), "lxml")
        print(match_info(s), '\n\n', match_stats(s), '\n')
    file.write('t_end =' + str(datetime.datetime.now()) + '\n' + 
               str(len(match_links)) + '\n')
file.close()
