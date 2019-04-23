# %%
import requests
import pandas
import os

#from config import proxies
from bs4 import BeautifulSoup

# %%
page = requests.get("http://www.howstat.com/cricket/Statistics/Matches/MatchListMenu.asp")

# %%
soup = BeautifulSoup(page.content, 'html.parser')

# %%
a_all = soup.select('#odis > table > tr > td > table > tr > td > a.LinkOff')
href_all = ['http://www.howstat.com/cricket/Statistics/Matches/' + a['href'] for a in a_all]

# %%
ds = []

for href in href_all:
    print(href)
    
    page = requests.get(href)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    tr_all = soup.select('table.TableLined > tr')
    tr_all = tr_all[1:]
    
    for tr in tr_all:
        td_all = tr.select('td')
        
        date = td_all[1].text.strip()
        countries = td_all[2].text.strip()
        ground = td_all[3].text.strip()
        result = td_all[4].text.strip()
        
        ds.append([date, countries, ground, result])

# %%
columns = [
        'DATE',
        'COUNTRIES',
        'GROUND',
        'RESULT']

if not os.path.exists('files'):
    os.mkdir('files')

df = pandas.DataFrame(data = ds, columns = columns)
df.to_csv('files/matches.txt', sep = '|', index = False)
