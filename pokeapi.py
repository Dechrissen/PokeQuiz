import urllib.request
from urllib.request import urlopen
from json import loads


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


for n in range(400, 408):
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
        
    print(name, gen, preevo)
