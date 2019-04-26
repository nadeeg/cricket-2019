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
dg = pandas.read_csv('files/match_player_features.txt', '|')
dd = dict(tuple(dg.groupby(['DATE', 'COUNTRIES','GROUND'])))

# %%
for r1 in df.itertuples():
    dp = dd[(r1.DATE, r1.COUNTRIES, r1.GROUND)]
    dp = dp.sort_values(by = ['TEAM', 'NUM_OF_MATCH', 'PLAYER_NAME'],\
                        ascending = [1, 0, 1])

    dq = dp[dp['TEAM'] == 0]
    for i in range(0, 11):
        col = 'Bat.1.' + str(i)
        df.at[r1.Index, col] = dq.iloc[i].NUM_OF_MATCH

    dq = dp[dp['TEAM'] == 1]
    for i in range(0, 11):
        col = 'Bat.2.' + str(i)
        df.at[r1.Index, col] = dq.iloc[i].NUM_OF_MATCH

# %%
dh = df.reindex(columns = ['DATE', 'GROUND', 'CITY', 'COUNTRY',
                           'TEAM.1', 'TEAM.2', 'IS_HOST.1', 'IS_HOST.2',
                           'Bat.1.0', 'Bat.1.1', 'Bat.1.2', 'Bat.1.3',
                           'Bat.1.4', 'Bat.1.5', 'Bat.1.6', 'Bat.1.7',
                           'Bat.1.8', 'Bat.1.9', 'Bat.1.10',
                           'Bat.2.0', 'Bat.2.1', 'Bat.2.2', 'Bat.2.3',
                           'Bat.2.4', 'Bat.2.5', 'Bat.2.6', 'Bat.2.7',
                           'Bat.2.8', 'Bat.2.9', 'Bat.2.10',
                           'WINNER', 'MARGIN', 'Y'])

# %%
if not os.path.exists('trainset'):
    os.mkdir('trainset')

df.to_csv('trainset/input.txt', sep = '|', index = False)
