import sqlite3

teams = ['Team Rocket', 'Team Magma', 'Team Aqua', 'Team Galactic', 'Team Plasma', 'Team Flare', 'Team Skull', 'Aether Foundation', 'Team Yell']
bosses = ['Giovanni', 'Maxie', 'Archie', 'Cyrus', 'N', 'Lysandre', 'Guzma', 'Lusamine', 'Piers']
regions = ['Kanto', 'Hoenn', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Alola', 'Galar']

conn = sqlite3.connect('pokequiz.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS teams')
cur.execute('CREATE TABLE teams (name TEXT, boss TEXT, region TEXT)')
for i in range(len(teams)):
    cur.execute('INSERT INTO teams (name, boss, region) VALUES (?, ?, ?)', (teams[i], bosses[i], regions[i]))

conn.commit()
conn.close()
