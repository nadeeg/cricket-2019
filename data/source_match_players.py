# %%
import requests
import pandas
import os
import re

from bs4 import BeautifulSoup

# %%
page = requests.get('http://www.howstat.com/cricket/Statistics/Matches/MatchListMenu.asp')

# %%
soup = BeautifulSoup(page.content, 'html.parser')

# %%
a_all = soup.select('#odis > table > tr > td > table > tr > td > a.LinkOff')
a_all = [a for a in a_all if not a.text.strip().endswith('World Cup')]
href_all = ['http://www.howstat.com/cricket/Statistics/Matches/' + a['href'] for a in a_all]

# %%
match_info = []

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
        a_scorecard = td_all[5].select_one('a')
        
        match_info.append([date, countries, ground, 'http://www.howstat.com/cricket/Statistics/Matches/' + a_scorecard['href'] + '&Print=Y', href])
# %%
def is_aborted(soup):
    td = soup.select_one('body > table:nth-child(2) > tr:nth-child(1) > td > table > tr:nth-child(5) > td.TextBlack8')
    return td is not None and (td.text.strip() == 'Match abandoned' or\
                               td.text.strip() == 'Match cancelled' or\
                               td.text.strip() == 'No result')

def is_conceded(soup):
    td = soup.select_one('body > table:nth-child(2) > tr:nth-child(1) > td > table > tr:nth-child(5) > td.TextBlack8')
    return td is not None and (td.text.strip().endswith('won by default') or\
                               td.text.strip().endswith('won by walkover'))

def is_innings_start(td_all):
    return len(td_all) == 7 and td_all[1].text.strip() == 'R' and td_all[2].text.strip() == 'BF'

def is_innings_stop(td_all):
    return len(td_all) < 7

# %%
ds = []
count = 0

for info in match_info:
    date, countries, ground, href, parent_href = info
    
    count += 1
    print(count)
    print(parent_href)
    print(href)
    
    page = requests.get(href)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    table = soup.select_one('body > table:nth-child(2) > tr > td > table:nth-child(3)')
    
    if is_aborted(soup):
        print('Detect match aborted')
        continue
    elif is_conceded(soup):
        print('Detect match conceded')
        continue
    elif table is None:
        print('Possibly match aborted')
        break
    
    tr_all = table.select('tr')
    
    dt = []
    
    innings_start = False
    team = 0
    for tr in tr_all:
        td_all = tr.select('td')
        
        if innings_start and is_innings_stop(td_all):
            innings_start = False
            team += 1
        
        if innings_start:
            a = td_all[0].select_one('a')
            player_id = re.sub(r'(.*)=(.*)', r'\2', a['href'])
            player_name = td_all[0].text.strip()
            dt.append([date, countries, ground, team, player_name, player_id])
        
        if is_innings_start(td_all):
            innings_start = True
        
        if team > 1:
            break
    
    if team == 1:
        tr_all = soup.select('body > table:nth-child(2) > tr')
        
        for tr in tr_all:
            td_all = tr.select('td')
            
            if innings_start and is_innings_stop(td_all):
                innings_start = False
                team += 1
            
            if innings_start:
                a = td_all[0].select_one('a')
                player_id = re.sub(r'(.*)=(.*)', r'\2', a['href'])
                player_name = td_all[0].text.strip()
                dt.append([date, countries, ground, team, player_name, player_id])
            
            if is_innings_start(td_all):
                innings_start = True
            
            if team > 1:
                break
    
    if len(dt) != 22:
        print('Less than 22 players, possibly scrap error')
    
    ds.extend(dt)

# %%
columns = [
        'DATE',
        'COUNTRIES',
        'GROUND',
        'TEAM',
        'PLAYER_NAME',
        'PLAYER_ID']

if not os.path.exists('files'):
    os.mkdir('files')

df = pandas.DataFrame(data = ds, columns = columns)
df.to_csv('files/match_players.txt', sep = '|', index = False)
