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

    for n in range(300, 305 + 1):
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
        # create types list
        if type2:
            types = [type1, type2]
        else:
            types = [type1]
        # stringify types list
        types = json.dumps(types)
        # insert Pokemon data into table
        cur.execute('DROP TABLE IF EXISTS pokemon')
        cur.execute('CREATE TABLE pokemon (name TEXT, preevo TEXT, types TEXT, gen TEXT)')
        cur.execute('INSERT INTO pokemon (name, preevo, types, gen) VALUES (?, ?, ?, ?)')
        print("Wrote", n, "to database")
    print("Done")

def fillTeams():
    print("Starting teams table fill...")
    # Create Teams table
    teams = ['Team Rocket', 'Team Magma', 'Team Aqua', 'Team Galactic', 'Team Plasma', 'Team Flare', 'Team Skull', 'Aether Foundation', 'Team Yell']
    bosses = ['Giovanni', 'Maxie', 'Archie', 'Cyrus', 'N', 'Lysandre', 'Guzma', 'Lusamine', 'Piers']
    gens = ['1', '3', '3', '4', '5', '6', '7', '7', '8']
    regions = ['Kanto', 'Hoenn', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Alola', 'Galar']

    cur.execute('DROP TABLE IF EXISTS teams')
    cur.execute('CREATE TABLE teams (name TEXT, boss TEXT, region TEXT, gen TEXT)')
    for i in range(len(teams)):
        cur.execute('INSERT INTO teams (name, boss, region, gen) VALUES (?, ?, ?, ?)', (teams[i], bosses[i], regions[i], gens[i]))
    print("Done")

def fillGames():
    print("Starting games table fill...")
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
    print("Done")

def fillRegions():
    print("Starting regions table fill...")
    regions = {1 : ['Kanto', '1', ['Pallet Town','Viridian City','Pewter City','Cerulean City','Vermilion City','Lavender Town','Celadon City','Fuchsia City','Saffron City','Cinnabar Island'],
                ["Cerulean Cave","Diglett's Cave",'Indigo Plateau','Mt. Moon', 'Cycling Road', 'Silence Bridge', 'Pokemon Mansion','Pokemon Tower','Rock Tunnel','SS Anne', 'Tohjo Falls', 'Team Rocket Hideout', 'Fuschia Safari Zone','Seafoam Islands','Silph Co.','Victory Road','Viridian Forest'],
                'Oak'],
               2 : ['Johto', '2', ["New Bark Town","Cherrygrove City","Violet City","Azalea Town","Goldenrod City","Ecruteak City","Olivine City","Cianwood City","Mahogany Town","Blackthorn City"],
               ["Dark Cave", "Sprout Tower", "Ruins of Alph", "Union Cave", "Ilex Forest", "Radio Tower","Team Rocket HQ","National Park","SS Aqua", "Tin Tower", "Bellchime Trail", "Burned Tower", "Moomoo Farm", "Glitter Lighthouse", "Whirl Islands", "Mt. Mortar", "Lake of Rage", "Ice Path", "Dragon's Den", "Mt. Silver"],
               'Elm'],
               3 : ['Hoenn', '3', ['Littleroot Town','Oldale Town','Petalburg City','Rustboro City','Dewford Town','Slateport City','Mauville City','Verdanturf Town','Fallarbor Town',
               'Lavaridge Town','Fortree City','Lilycove City','Mossdeep City','Sootopolis City','Pacifidlog Town','Ever Grande City'],
               ["Petalburg Woods", "Rusturf Tunnel", "Island Cave", "Granite Cave", "Abandoned Ship", "Sea Mauville", "Oceanic Museum",
               "Seaside Cycling Road", "Trick House", "New Mauville", "Trainer Hill", "Desert Ruins", "Mirage Tower", "Fiery Path",
               "Jagged Pass", "Mt. Chimney", "Desert Underpass", "Meteor Falls", "Weather Institute", "Scorched Slab", "Ancient Tomb", "Route 121 Safari Zone", "Mt. Pyre",
               "Lilycove Museum", "Shoal Cave", "Space Center", "Seafloor Cavern","Cave of Origin", "Mirage Island", "Sky Pillar", "Sealed Chamber", "Artisan Cave",
               "Altering Cave", "Southern Island", "Marine Cave", "Terra Cave"], 'Birch'],
               4 : ['Sinnoh', '4', ["Twinleaf Town","Sandgem Town","Jubilife City","Oreburgh City","Floaroma Town","Eterna City","Hearthome City",
               "Solaceon Town","Veilstone City","Pastoria City","Celestic Town","Canalave City","Snowpoint City",
               "Sunyshore City"], ["Lake Verity", "Oreburgh Gate", "Oreburgh Mine", "Ravaged Path",
               "Floaroma Meadow", "Valley Windworks", "Eterna Forest", "Old Chateau", "Wayward Cave", "Mt. Coronet",
               "Amity Square", "Lost Tower", "Hallowed Tower", "Solaceon Ruins", "Maniac Tunnel", "Lake Valor", "Great Marsh", "Trophy Garden", "Fuego Ironworks",
               "Iron Island", "Lake Acuity", "Spear Pillar","Resort Area", "Fight Area", "Survival Area", "Stark Mountain", "Snowpoint Temple",
               "Spring Path", "Sendoff Spring", "Turnback Cave", "Fullmoon Island", "Newmoon Island", "Seabreak Path", "Flower Paradise", "Hall of Origin"], 'Rowan'],
               5 : ['Unova', '5', ["Accumula Town","Anville Town","Aspertia City","Black City","Castelia City","Driftveil City","Floccesy Town",
               "Humilau City","Icirrus City","Lacunosa Town","Lentimas Town","Mistralton City","Nacrene City","Nimbasa City",
               "Nuvema Town","Opelucid City","Striaton City","Undella Town","Virbank City","White Forest"], ["Dreamyard", "Wellspring Cave", "Pinwheel Forest", "Liberty Garden", "Desert Resort", "Relic Castle", "Battle Subway", "Lostlorn Forest",
               "Cold Storage", "Mistralton Cave", "Chargestone Cave", "Celestial Tower", "Twist Mountain", "Dragonspiral Tower", "Moor of Icirrus",
               "Challenger's Cave", "N's Castle", "Royal Unova", "Giant Chasm", "Undella Bay", "Abyssal Ruins",
               "Abundant Shrine", "P2 Laboratory", "Entralink", "Unity Tower", "Floccesy Ranch", "Pledge Grove", "Virbank Complex",
               "Pokestar Studios", "Castelia Sewers", "Join Avenue", "Cave of Being", "Pokemon World Tournament", "Reversal Mountain", "Plasma Frigate",
               "Clay Tunnel", "Underground Ruins", "Strange House", "Relic Passage", "Seaside Cave", "White Treehollow", "Black Tower",
               "Skyarrow Bridge", "Driftveil Drawbridge", "Tubeline Bridge", "Village Bridge", "Marvelous Bridge", "Marine Tube"], 'Juniper'],
               6 : ['Kalos', '6', ["Ambrette Town","Anistar City","Aquacorde Town","Camphrier Town","Coumarine City","Couriway Town","Cyllage City","Dendemille Town",
               "Geosenge Town","Kiloude City","Laverre City","Lumiose City","Santalune City","Shalour City","Snowbelle City","Vaniville Town"], ["Santalune Forest",
               "Chamber of Emptiness", "Parfum Palace", "Battle Chateau", "Connecting Cave", "Glittering Cave", "Reflection Cave",
               "Tower of Mastery", "Azure Bay", "Sea Spirit's Den", "Poke Ball Factory", "Lost Hotel", "Frost Cavern", "Lysandre Labs",
                "Terminus Cave", "Pokemon Village"], 'Sycamore'],
                7 : ['Alola', '7', ["Hau'oli City","Heahea City","Iki Town","Konikoni City","Malie City","Paniola Town","Po Town",
                "Seafolk Village","Tapu Village"], ["Mahalo Trail", "Hau'oli Cemetery", "Verdant Cavern", "Melemele Meadow", "Seaward Cave", "Kala'e Bay",
                "Ten Carat Hill", "Paniola Ranch", "Brooklet Hill", "Melemele Sea", "Diglett's Tunnel", "Royal Avenue", "Battle Royal Dome", "Wela Volcano Park",
                "Lush Jungle", "Memorial Hill", "Akala Outskirts", "Ruins of Life", "Hano Grand Resort", "Hano Beach", "Malie Garden", "Mount Hokulani",
                "Hokulani Observatory", "Blush Mountain", "Ula'ula Beach", "Aether House", "Haina Desert",
                "Ruins of Abundance", "Ula'ula Meadow", "Lake of the Moone", "Lake of the Sunne", "Shady House", "Poni Wilds", "Ancient Poni Path",
                "Poni Breaker Coast", "Ruins of Hope", "Exeggutor Island", "Vast Poni Canyon", "Altar of the Sunne", "Altar of the Moone", "Mount Lanakila",
                "Ruins of Conflict", "Poni Grove", "Poni Plains", "Poni Meadow", "Resolution Cave", "Poni Coast", "Poni Gauntlet", "Battle Tree",
                "Festival Plaza", "Poke Pelago", "Big Wave Beach", "Sandy Cave", "Heahea Beach", "Pikachu Valley", "Dividing Peak Tunnel",
                "Kantonian Gym", "Poni Beach", "Plains Grotto", "Team Rocket's Castle"], 'Kukui']}
    cur.execute('DROP TABLE IF EXISTS regions')
    cur.execute('CREATE TABLE regions (name TEXT, gen TEXT, towns TEXT, landmarks TEXT, professor TEXT)')
    for i in regions.keys():
        cur.execute('INSERT INTO games (name, gen, towns, landmarks, professor) VALUES (?, ?, ?, ?, ?)', (regions[i][0], regions[i][1], json.dumps(regions[i][2]), json.dumps(regions[i][3]), regions[i][4]))
    print("Done")

def fillTowns():
    print("Starting towns table fill...")
    towns = {1 : ['Pallet Town', 'Kanto', [], '1'],
             2 : ['Viridian City', 'Kanto', ['Giovanni', 'Blue'], '1'],
             3 : ['Pewter City', 'Kanto', ['Brock'], '1'],
             4 : ['Cerulean City', 'Kanto', ['Misty'], '1'],
             5 : ['Vermilion City', 'Kanto', ['Lt. Surge'], '1'],
             6 : ['Lavender Town', 'Kanto', [], '1'],
             7 : ['Celadon City', 'Kanto', ['Erika'], '1'],
             8 : ['Fuchsia City', 'Kanto', ['Koga', 'Janine'], '1'],
             9 : ['Saffron City', 'Kanto', ['Sabrina'], '1'],
             10 : ['Cinnabar Island', 'Kanto', ['Blaine'], '1'],
             10 : ['New Bark Town', 'Johto', [], '2'],
             10 : ['Cherrygrove City', 'Johto', [], '2'],
             10 : ['Violet City', 'Johto', ['Falkner'], '2'],
             10 : ['Azalea Town', 'Johto', ['Bugsy'], '2'],
             10 : ['Goldenrod City', 'Johto', ['Whitney'], '2'],
             10 : ['Ecruteak City', 'Johto', ['Morty'], '2'],
             10 : ['Olivine City', 'Johto', ['Jasmine'], '2'],
             10 : ['Cianwood City', 'Johto', ['Chuck'], '2'],
             10 : ['Mahogany Town', 'Johto', ['Pryce'], '2'],
             10 : ['Blackthorn City', 'Johto', ['Clair'], '2'],
             10 : ['Littleroot Town', 'Hoenn', [], '3'],
             10 : ['Oldale Town', 'Hoenn', [], '3'],
             10 : ['Petalburg City', 'Hoenn', ['Norman'], '3'],
             10 : ['Rustboro City', 'Hoenn', ['Roxanne'], '3'],
             10 : ['Dewford Town', 'Hoenn', ['Brawly'], '3'],
             10 : ['Slateport City', 'Hoenn', [], '3'],
             10 : ['Mauville City', 'Hoenn', ['Wattson'], '3'],
             10 : ['Verdanturf Town', 'Hoenn', [], '3'],
             10 : ['Fallarbor Town', 'Hoenn', [], '3'],
             10 : ['Lavaridge Town', 'Hoenn', ['Flannery'], '3'],
             10 : ['Fortree City', 'Hoenn', ['Winona'], '3'],
             10 : ['Lilycove City', 'Hoenn', [], '3'],
             10 : ['Mossdeep City', 'Hoenn', ['Tate and Liza'], '3'],
             10 : ['Sootopolis City', 'Hoenn', ['Wallace', 'Juan'], '3'],
             10 : ['Pacifidlog Town', 'Hoenn', [], '3'],
             10 : ['Ever Grande City', 'Hoenn', [], '3'],}



# Start database population / API scraping
# Open connection to sqlite file
conn = sqlite3.connect('pokequiz.sqlite')
cur = conn.cursor()

# Uncomment functions below to fill corresponding tables
#fillPokemon()
#fillTeams()
#fillGames()
#fillRegions()

# Commit additions and close connection
conn.commit()

#test stuff
cur.execute('SELECT rivals FROM games ORDER BY RANDOM() LIMIT 1;')
for row in cur:
    j = json.loads(row[0])
    print(type(j))
    print(j)

# Close connection to db
conn.close()
