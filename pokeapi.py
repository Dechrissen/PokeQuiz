import urllib.request
from urllib.request import urlopen
from json import loads
import sqlite3


def fillPokemon():
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

    for n in range(230, 236):
        # Get species JSON
        req = urllib.request.Request(url.format(str(n)), headers=hdr)
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
        req = urllib.request.Request(pokemon_url, headers=hdr)
        response = urllib.request.urlopen(req)
        readable = response.read().decode('utf-8')
        obj = loads(readable)
        types = [obj['types'][i]['type']['name'] for i in range(len(obj['types']))]
        type1 = types[0]
        try:
            type2 = types[1]
        except IndexError:
            type2 = None
        print(name, preevo, type1, type2, gen)

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

# Start database population / API scraping
# Open connection to sqlite file
conn = sqlite3.connect('pokequiz.sqlite')
cur = conn.cursor()

# Uncomment functions below to fill corresponding tables
fillPokemon()
#fillTeams()

# Commit additions and close connection
conn.commit()
conn.close()
