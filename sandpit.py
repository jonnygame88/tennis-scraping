from bs4 import BeautifulSoup
import urllib.request as urlr
import pandas as pd
pd.set_option("display.width", 1000)

def fs(url):
    page = urlr.urlopen(url)
    return(BeautifulSoup(page.read(), "lxml"))

t_url = "http://www.tennisbetsite.com/players/atp/andy-murray.html?year=2015"
soup = fs(t_url)
table = soup.find( "table", {"class": "results"} )
rows = [tr.findAll('td') for tr in table.findAll("tr")]
headers = table.findAll("th")

links = [tr.findAll("a") for tr in table.findAll("tr")]
dates = [tr.findAll("td", {"class": "date"}) for tr in table.findAll("tr")]

for x in rows[63]: print(x.get_text())
for x in dates[63]: print(x.get_text())
for x in links[63]: print(x.get("href"))

## function: date, opponent url, match url
