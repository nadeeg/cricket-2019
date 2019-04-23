# %%
import pandas
import os

# %%
df = pandas.read_csv('files/matches_formatted.txt', '|')

dg = df.reindex(columns = ['DATE', 'TEAM1', 'TEAM2'])

dg.rename(columns = { 'TEAM1': 'TEAM.1', 'TEAM2': 'TEAM.2'}, inplace = True)

dg['IS_HOST.1'] = (dg['TEAM.1'] == df['Country'])
dg['IS_HOST.2'] = (dg['TEAM.2'] == df['Country'])

dg['Y'] = (dg['TEAM.1'] == df['WINNER'])
# %%
ds =[]

for row in dg.itertuples():
    print(row)
    break

#%%
columns = [
        'DATE',
        'TEAM.1',
        'TEAM.2',
        'IS_HOST.1',
        'IS_HOST.2',
        'Y',]

if not os.path.exists('trainset'):
    os.mkdir('trainset')

dg.to_csv('trainset/input.txt', sep = '|', index = False)
