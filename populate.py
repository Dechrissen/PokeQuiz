# This script is used to collect data from PokeAPI and populate SQLite database tables.
# There is one function per data table to be filled.
import urllib.request
from urllib.request import urlopen
from json import loads
import sqlite3
import time
import json


def fillPokemon():
    print("Starting PokeAPI scrape to populate Pokemon table...")
    # Scrape PokeAPI for Pokemon data
    url = "http://pokeapi.co/api/v2/pokemon-species/{}/"
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'pokeapi.co',
    'TE': 'Trailers',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'dechrissen'
    }

    for n in range(290, 295 + 1):
        # Get species JSON
        try:
            req = urllib.request.Request(url.format(str(n)), headers=hdr)
        # redo the current iteration if the request failed
        except urllib.error.HTTPError:
            print("Iteration", n, "failed. Sleeping (60) ...")
            n = n - 1
            time.sleep(60)
            continue
        response = urllib.request.urlopen(req)
        readable = response.read().decode('utf-8')
        obj = loads(readable)
        # Save variables (name, gen, preevo)
        name = obj['name']
        gen = obj['generation']['url'].split('generation/')[1].strip('/')
        try:
            preevo = obj['evolves_from_species']['name']
        except TypeError:
            preevo = None
        # Now get Pokemon JSON for types
        pokemon_url = obj['varieties'][0]['pokemon']['url']
        try:
            req = urllib.request.Request(pokemon_url, headers=hdr)
        # redo the current iteration if the request failed
        except urllib.error.HTTPError:
            print("Iteration", n, "failed. Sleeping (60) ...")
            n = n - 1
            time.sleep(60)
            continue
        response = urllib.request.urlopen(req)
        readable = response.read().decode('utf-8')
        obj = loads(readable)
        # save types
        types = [obj['types'][i]['type']['name'] for i in range(len(obj['types']))]
        type1 = types[0]
        try:
            type2 = types[1]
        except IndexError:
            type2 = None
        print(name, preevo, type1, type2, gen)
        print("Wrote", n, "to database")

def fillTeams():
    # Create Teams table
    teams = ['Team Rocket', 'Team Magma', 'Team Aqua', 'Team Galactic', 'Team Plasma', 'Team Flare', 'Team Skull', 'Aether Foundation', 'Team Yell']
    bosses = ['Giovanni', 'Maxie', 'Archie', 'Cyrus', 'N', 'Lysandre', 'Guzma', 'Lusamine', 'Piers']
    gens = ['1', '3', '3', '4', '5', '6', '7', '7', '8']
    regions = ['Kanto', 'Hoenn', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Alola', 'Galar']

    cur.execute('DROP TABLE IF EXISTS teams')
    cur.execute('CREATE TABLE teams (name TEXT, boss TEXT, region TEXT, gen TEXT)')
    for i in range(len(teams)):
        cur.execute('INSERT INTO teams (name, boss, region, gen) VALUES (?, ?, ?, ?)', (teams[i], bosses[i], regions[i], gens[i]))

def fillGames():
    games = {1 : ['Red & Blue', 'Kanto', '1', ['Blue'], 'Blue'],
             2 : ['Yellow', 'Kanto', '1', ['Blue'], 'Blue'],
             3 : ['Gold & Silver', 'Johto', '2', ['Silver'], 'Lance'],
             4 : ['Crystal', 'Johto', '2', ['Silver'], 'Lance'],
             5 : ['Ruby & Sapphire', 'Hoenn', '3', ['Brendan', 'May', 'Wally'], 'Steven'],
             6 : ['Emerald', 'Hoenn', '3', ['Brendan', 'May', 'Wally'], 'Wallace'],
             7 : ['FireRed & LeafGreen', 'Kanto', '3', ['Blue'], 'Blue'],
             8 : ['Diamond & Pearl', 'Sinnoh', '4', ['Barry'], 'Cynthia'],
             9 : ['Platinum', 'Sinnoh', '4', ['Barry'], 'Cynthia'],
             10 : ['HeartGold & SoulSilver', 'Johto', '4', ['Silver'], 'Lance'],
             11 : ['Black & White', 'Unova', '5', ['Cheren', 'Bianca'], 'Alder'],
             12 : ['Black 2 & White 2', 'Unova', '5', ['Hugh'], 'Iris'],
             13 : ['X & Y', 'Kalos', '6', ['Calem', 'Serena', 'Shauna', 'Tierno', 'Trevor'], 'Diantha'],
             14 : ['Omega Ruby & Alpha Sapphire', 'Hoenn', '6', ['Brendan', 'May', 'Wally'], 'Steven'],
             15 : ['Sun & Moon', 'Alola', '7', ['Hau', 'Gladion'], 'Kukui'],
             16 : ['Ultra Sun & Ultra Moon', 'Alola', '7', ['Hau', 'Gladion'], 'Hau']}
    cur.execute('DROP TABLE IF EXISTS games')
    cur.execute('CREATE TABLE games (name TEXT, region TEXT, gen TEXT, rivals TEXT, champion TEXT)')
    for i in games.keys():
        cur.execute('INSERT INTO games (name, region, gen, rivals, champion) VALUES (?, ?, ?, ?, ?)', (games[i][0], games[i][1], games[i][2], json.dumps(games[i][3]), games[i][4]))


# Start database population / API scraping
# Open connection to sqlite file
conn = sqlite3.connect('pokequiz.sqlite')
cur = conn.cursor()

# Uncomment functions below to fill corresponding tables
#fillPokemon()
#fillTeams()
fillGames()

# Commit additions and close connection
conn.commit()
cur.execute('SELECT rivals FROM games ORDER BY RANDOM() LIMIT 1;')
for row in cur:
    j = json.loads(row[0])
    print(type(j))
    print(j)


conn.close()
