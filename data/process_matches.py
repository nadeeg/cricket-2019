# %%
import pandas
import re
import os

# %%
df = pandas.read_csv('files/matches.txt', '|')
dg = pandas.read_csv('files/grounds.txt', '|')

# %%
df = df[df['RESULT'] != 'No result']
df = df[df['RESULT'] != 'Match abandoned']
df = df[df['RESULT'] != 'Match cancelled']
df = df[~(df['RESULT'].str.contains('conceded'))]
df = df[~(df['RESULT'].str.endswith('won by default'))]
df = df[~(df['RESULT'].str.endswith('won by walkover'))]

# %%
dd = dict(tuple(dg.groupby(['GROUND'])))

# %%
compiled = re.compile(r'(.*)/(.*)/(.*)')

for row in df.itertuples():
    df.at[row.Index, 'DATE'] = compiled.sub(r'\3-\2-\1', row.DATE)
    
    countries = row.COUNTRIES.split('v.')
    c1 = countries[0].strip()
    c2 = countries[1].strip()
    df.at[row.Index, 'TEAM.1'] = c1
    df.at[row.Index, 'TEAM.2'] = c2
    
    if row.RESULT == 'Match Tied':
        winner = None
        margin = 'Tied'
    else:
        results = row.RESULT.split(' won by ')
        winner = results[0].strip()
        margin = results[1].strip()
    df.at[row.Index, 'WINNER'] = winner
    df.at[row.Index, 'MARGIN'] = margin
    
    df.at[row.Index, 'CITY'] = dd[row.GROUND].iloc[0]['CITY']
    df.at[row.Index, 'COUNTRY'] = dd[row.GROUND].iloc[0]['COUNTRY']

# %%
dh = df.reindex(columns = ['DATE', 'COUNTRIES', 'GROUND', 'CITY', 'COUNTRY',\
                           'TEAM.1', 'TEAM.2', 'WINNER', 'MARGIN'])

# %%
if not os.path.exists('files'):
    os.mkdir('files')

dh.to_csv('files/matches_formatted.txt', sep = '|', index = False)
