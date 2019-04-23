import pandas as pd
import csv

# %%
matches = pd.read_csv('files/matches.txt', sep = '|')

with open('files/grounds.csv', 'rt') as f:
  reader = csv.reader(f)
  data = []

  for row in reader:
      data.append(row)
        
grounds = pd.DataFrame(columns = data[0], data = data[1:])

# %%
matches['DATE'] = pd.to_datetime(matches['DATE'], format = '%d/%m/%Y')
matches['TEAM1'] = matches['COUNTRIES'].str.split('v.').str[0]
matches['TEAM2'] = matches['COUNTRIES'].str.split('v.').str[1]
matches['TEAM1'] = matches['TEAM1'].str.strip()
matches['TEAM2'] = matches['TEAM2'].str.strip()
matches['WINNER'] = matches['RESULT'].str.split(' won by ').str[0]
matches['MARGIN'] = matches['RESULT'].str.split(' won by ').str[1]

# %%
matches = matches.merge(grounds, left_on = 'GROUND', right_on = 'Official name')
del matches['City']

# %%
matches.to_csv('files/matches_formatted.txt', sep = '|', index = False)
