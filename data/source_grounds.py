# %%
import requests
import pandas
import os
import re

from bs4 import BeautifulSoup

# %%
formData = {'cboCountry': 'XXX', 'optView': 'A'}
page = requests.get('http://www.howstat.com/cricket/Statistics/Grounds/GroundList.asp?Scope=O', data = formData)
soup = BeautifulSoup(page.content, 'html.parser')

# %%
table = soup.select_one('table.TableLined')
tr_all = table.select('tr')

# %%
ds = []

for tr in tr_all[1:-1]:
    td_all = tr.select('td')
    
    ground = td_all[0].text.strip()
    city = td_all[1].text.strip()
    country = td_all[2].text.strip()
    
    ds.append([ground, city, country])

# %%
columns = [
        'GROUND',
        'CITY',
        'COUNTRY']

if not os.path.exists('files'):
    os.mkdir('files')

df = pandas.DataFrame(data = ds, columns = columns)
df.to_csv('files/grounds.txt', sep = '|', index = False)
