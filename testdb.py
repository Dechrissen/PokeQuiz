import sqlite3


conn = sqlite3.connect('pokequiz.sqlite')
cur = conn.cursor()

# Create Teams table
teams = ['Team Rocket', 'Team Magma', 'Team Aqua', 'Team Galactic', 'Team Plasma', 'Team Flare', 'Team Skull', 'Aether Foundation', 'Team Yell']
bosses = ['Giovanni', 'Maxie', 'Archie', 'Cyrus', 'N', 'Lysandre', 'Guzma', 'Lusamine', 'Piers']
gens = ['1', '3', '3', '4', '5', '6', '7', '7', '8']
regions = ['Kanto', 'Hoenn', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Alola', 'Galar']

cur.execute('DROP TABLE IF EXISTS teams')
cur.execute('CREATE TABLE teams (name TEXT, boss TEXT, region TEXT, gen TEXT)')
for i in range(len(teams)):
    cur.execute('INSERT INTO teams (name, boss, region, gen) VALUES (?, ?, ?, ?)', (teams[i], bosses[i], regions[i], gens[i]))

# Create Pokemon table

# Create Regions table

# Create Towns table

# Create Leaders table

# Create Games table

conn.commit()
conn.close()
