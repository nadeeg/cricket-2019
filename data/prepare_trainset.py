# %%
import pandas
import os

# %%
df = pandas.read_csv('files/matches_formatted.txt', '|')

df['IS_HOST.1'] = (df['TEAM.1'] == df['COUNTRY']).astype('int')
df['IS_HOST.2'] = (df['TEAM.2'] == df['COUNTRY']).astype('int')

df['Y'] = (df['TEAM.1'] == df['WINNER']).astype('int')
df.loc[df['MARGIN'] == 'Tied', 'Y'] = 0.5

# %%

# %%
if not os.path.exists('trainset'):
    os.mkdir('trainset')

df.to_csv('trainset/input.txt', sep = '|', index = False)
