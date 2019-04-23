# %%
import requests
import pandas
import os

from config import proxies
from bs4 import BeautifulSoup

# %%
page = requests.get("http://www.howstat.com/cricket/Statistics/Players/PlayerListCurrent.asp", proxies=proxies)

# %%
soup = BeautifulSoup(page.content, 'html.parser')

# %%
table = soup.find('table', attrs = { 'class': 'TableLined' })
tr_all = table.find_all('tr')
tr_all = tr_all[2:-1]

# %%
ds = []

for tr in tr_all:
    td_all = tr.find_all('td')
    
    name = td_all[0].text.strip()
    born = td_all[1].text.strip()
    country = td_all[2].text.strip()
    test_count = td_all[3].text.strip() or '0'
    odi_count = td_all[4].text.strip() or '0'
    t20_count = td_all[5].text.strip() or '0'
    
    ds.append([name, born, country, test_count, odi_count, t20_count])

# %%
columns = [
        'NAME',
        'BORN',
        'COUNTRY',
        'TEST_COUNT',
        'ODI_COUNT',
        'T20_COUNT']

if not os.path.exists('files'):
    os.mkdir('files')

df = pandas.DataFrame(data = ds, columns = columns)
df.to_csv('files/players.txt', sep = '|', index = False)
