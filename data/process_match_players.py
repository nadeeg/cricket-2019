# %%
import pandas
import re
import os

# %%
df = pandas.read_csv('files/match_players.txt', '|')

compiled = re.compile(r'(.*)/(.*)/(.*)')

for row in df.itertuples():
    df.at[row.Index, 'DATE'] = compiled.sub(r'\3-\2-\1', row.DATE)

# %%
dd = dict(tuple(df.groupby(['DATE', 'COUNTRIES','GROUND'])))

# %%
df['NUM_OF_MATCH'] = 0

date = None
stats = {}

for key, df_match in sorted(dd.items()):
    for row in df_match.itertuples():
        if row.PLAYER_ID in stats:
            df.at[row.Index, 'NUM_OF_MATCH'] = stats[row.PLAYER_ID]
    for row in df_match.itertuples():
        if row.PLAYER_ID not in stats:
            stats[row.PLAYER_ID] = 0
        stats[row.PLAYER_ID] += 1

# %%
if not os.path.exists('files'):
    os.mkdir('files')

df.to_csv('files/match_player_features.txt', sep = '|', index = False)
