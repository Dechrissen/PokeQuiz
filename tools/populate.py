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
    # Create table
    cur.execute('DROP TABLE IF EXISTS pokemon')
    cur.execute('CREATE TABLE pokemon (name TEXT, preevo TEXT, types TEXT, gen TEXT)')
    # Scrape API
    for n in range(1, 807 + 1):
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
        # Correct Pokemon name
        name = name.replace('-', '').title()
        exceptions = ['Porygonz','Jangmoo','Hakamoo','Kommoo','Nidoranm','Nidoranf','Mimejr','Mrmime','Tapukoko','Tapulele','Tapubulu','Tapufini','Typenull','Hooh','Farfetchd']
        corrections = ['Porygon-Z','Jangmo-o','Hakamo-o','Kommo-o','Nidoran-M','Nidoran-F','Mime Jr.','Mr. Mime','Tapu Koko','Tapu Lele','Tapu Bulu','Tapu Fini','Type: Null','Ho-Oh',"Farfetch'd"]
        if name in exceptions:
            i = exceptions.index(name)
            name = corrections[i]
        gen = obj['generation']['url'].split('generation/')[1].strip('/')
        try:
            preevo = obj['evolves_from_species']['name']
        except TypeError:
            preevo = None
        # Correct preevo name
        if preevo:
            preevo = preevo.replace('-', '').title()
            if preevo in exceptions:
                i = exceptions.index(preevo)
                preevo = corrections[i]
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
        type1 = types[0].title()
        try:
            type2 = types[1].title()
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
        cur.execute('INSERT INTO pokemon (name, preevo, types, gen) VALUES (?, ?, ?, ?)', (name, preevo, types, gen))
        print("Wrote", n, "to database")
    print("Done")

def fillTeams():
    print("Starting teams table fill...")
    time.sleep(2)
    # Create Teams table
    teams = ['Team Rocket', 'Team Magma', 'Team Aqua', 'Team Galactic', 'Team Plasma', 'Team Flare', 'Team Skull', 'Aether Foundation']
    bosses = ['Giovanni', 'Maxie', 'Archie', 'Cyrus', 'N', 'Lysandre', 'Guzma', 'Lusamine']
    gens = ['1', '3', '3', '4', '5', '6', '7', '7']
    regions = ['Kanto', 'Hoenn', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Alola', 'Galar']

    cur.execute('DROP TABLE IF EXISTS teams')
    cur.execute('CREATE TABLE teams (name TEXT, boss TEXT, region TEXT, gen TEXT)')
    for i in range(len(teams)):
        cur.execute('INSERT INTO teams (name, boss, region, gen) VALUES (?, ?, ?, ?)', (teams[i], bosses[i], regions[i], gens[i]))
    print("Done")

def fillGames():
    print("Starting games table fill...")
    time.sleep(2)
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
    time.sleep(2)
    regions = {1 : ['Kanto', '1', ['Pallet Town','Viridian City','Pewter City','Cerulean City','Vermilion City','Lavender Town','Celadon City','Fuchsia City','Saffron City','Cinnabar Island'],
                ["Cerulean Cave","Diglett's Cave",'Indigo Plateau','Mt. Moon', 'Cycling Road', 'Silence Bridge', 'Pokemon Mansion','Pokemon Tower','Rock Tunnel','SS Anne', 'Tohjo Falls', 'Team Rocket Hideout', 'Fuschia Safari Zone','Seafoam Islands','Silph Co.','Victory Road','Viridian Forest'],
                'Professor Oak'],
               2 : ['Johto', '2', ["New Bark Town","Cherrygrove City","Violet City","Azalea Town","Goldenrod City","Ecruteak City","Olivine City","Cianwood City","Mahogany Town","Blackthorn City"],
               ["Dark Cave", "Sprout Tower", "Ruins of Alph", "Union Cave", "Ilex Forest", "Radio Tower","Team Rocket HQ","National Park","SS Aqua", "Tin Tower", "Bellchime Trail", "Burned Tower", "Moomoo Farm", "Glitter Lighthouse", "Whirl Islands", "Mt. Mortar", "Lake of Rage", "Ice Path", "Dragon's Den", "Mt. Silver"],
               'Professor Elm'],
               3 : ['Hoenn', '3', ['Littleroot Town','Oldale Town','Petalburg City','Rustboro City','Dewford Town','Slateport City','Mauville City','Verdanturf Town','Fallarbor Town',
               'Lavaridge Town','Fortree City','Lilycove City','Mossdeep City','Sootopolis City','Pacifidlog Town','Ever Grande City'],
               ["Petalburg Woods", "Rusturf Tunnel", "Island Cave", "Granite Cave", "Abandoned Ship", "Sea Mauville", "Oceanic Museum",
               "Seaside Cycling Road", "Trick House", "New Mauville", "Trainer Hill", "Desert Ruins", "Mirage Tower", "Fiery Path",
               "Jagged Pass", "Mt. Chimney", "Desert Underpass", "Meteor Falls", "Weather Institute", "Scorched Slab", "Ancient Tomb", "Route 121 Safari Zone", "Mt. Pyre",
               "Lilycove Museum", "Shoal Cave", "Space Center", "Seafloor Cavern","Cave of Origin", "Mirage Island", "Sky Pillar", "Sealed Chamber", "Artisan Cave",
               "Altering Cave", "Southern Island", "Marine Cave", "Terra Cave"], 'Professor Birch'],
               4 : ['Sinnoh', '4', ["Twinleaf Town","Sandgem Town","Jubilife City","Oreburgh City","Floaroma Town","Eterna City","Hearthome City",
               "Solaceon Town","Veilstone City","Pastoria City","Celestic Town","Canalave City","Snowpoint City",
               "Sunyshore City"], ["Lake Verity", "Oreburgh Gate", "Oreburgh Mine", "Ravaged Path",
               "Floaroma Meadow", "Valley Windworks", "Eterna Forest", "Old Chateau", "Wayward Cave", "Mt. Coronet",
               "Amity Square", "Lost Tower", "Hallowed Tower", "Solaceon Ruins", "Maniac Tunnel", "Lake Valor", "Great Marsh", "Trophy Garden", "Fuego Ironworks",
               "Iron Island", "Lake Acuity", "Spear Pillar","Resort Area", "Fight Area", "Survival Area", "Stark Mountain", "Snowpoint Temple",
               "Spring Path", "Sendoff Spring", "Turnback Cave", "Fullmoon Island", "Newmoon Island", "Seabreak Path", "Flower Paradise", "Hall of Origin"], 'Professor Rowan'],
               5 : ['Unova', '5', ["Accumula Town","Anville Town","Aspertia City","Black City","Castelia City","Driftveil City","Floccesy Town",
               "Humilau City","Icirrus City","Lacunosa Town","Lentimas Town","Mistralton City","Nacrene City","Nimbasa City",
               "Nuvema Town","Opelucid City","Striaton City","Undella Town","Virbank City","White Forest"], ["Dreamyard", "Wellspring Cave", "Pinwheel Forest", "Liberty Garden", "Desert Resort", "Relic Castle", "Battle Subway", "Lostlorn Forest",
               "Cold Storage", "Mistralton Cave", "Chargestone Cave", "Celestial Tower", "Twist Mountain", "Dragonspiral Tower", "Moor of Icirrus",
               "Challenger's Cave", "N's Castle", "Royal Unova", "Giant Chasm", "Undella Bay", "Abyssal Ruins",
               "Abundant Shrine", "P2 Laboratory", "Entralink", "Unity Tower", "Floccesy Ranch", "Pledge Grove", "Virbank Complex",
               "Pokestar Studios", "Castelia Sewers", "Join Avenue", "Cave of Being", "Pokemon World Tournament", "Reversal Mountain", "Plasma Frigate",
               "Clay Tunnel", "Underground Ruins", "Strange House", "Relic Passage", "Seaside Cave", "White Treehollow", "Black Tower",
               "Skyarrow Bridge", "Driftveil Drawbridge", "Tubeline Bridge", "Village Bridge", "Marvelous Bridge", "Marine Tube"], 'Professor Juniper'],
               6 : ['Kalos', '6', ["Ambrette Town","Anistar City","Aquacorde Town","Camphrier Town","Coumarine City","Couriway Town","Cyllage City","Dendemille Town",
               "Geosenge Town","Kiloude City","Laverre City","Lumiose City","Santalune City","Shalour City","Snowbelle City","Vaniville Town"], ["Santalune Forest",
               "Chamber of Emptiness", "Parfum Palace", "Battle Chateau", "Connecting Cave", "Glittering Cave", "Reflection Cave",
               "Tower of Mastery", "Azure Bay", "Sea Spirit's Den", "Poke Ball Factory", "Lost Hotel", "Frost Cavern", "Lysandre Labs",
                "Terminus Cave", "Pokemon Village"], 'Professor Sycamore'],
                7 : ['Alola', '7', ["Hau'oli City","Heahea City","Iki Town","Konikoni City","Malie City","Paniola Town","Po Town",
                "Seafolk Village","Tapu Village"], ["Mahalo Trail", "Hau'oli Cemetery", "Verdant Cavern", "Melemele Meadow", "Seaward Cave", "Kala'e Bay",
                "Ten Carat Hill", "Paniola Ranch", "Brooklet Hill", "Melemele Sea", "Diglett's Tunnel", "Royal Avenue", "Battle Royal Dome", "Wela Volcano Park",
                "Lush Jungle", "Memorial Hill", "Akala Outskirts", "Ruins of Life", "Hano Grand Resort", "Hano Beach", "Malie Garden", "Mount Hokulani",
                "Hokulani Observatory", "Blush Mountain", "Ula'ula Beach", "Aether House", "Haina Desert",
                "Ruins of Abundance", "Ula'ula Meadow", "Lake of the Moone", "Lake of the Sunne", "Shady House", "Poni Wilds", "Ancient Poni Path",
                "Poni Breaker Coast", "Ruins of Hope", "Exeggutor Island", "Vast Poni Canyon", "Altar of the Sunne", "Altar of the Moone", "Mount Lanakila",
                "Ruins of Conflict", "Poni Grove", "Poni Plains", "Poni Meadow", "Resolution Cave", "Poni Coast", "Poni Gauntlet", "Battle Tree",
                "Festival Plaza", "Poke Pelago", "Big Wave Beach", "Sandy Cave", "Heahea Beach", "Pikachu Valley", "Dividing Peak Tunnel",
                "Kantonian Gym", "Poni Beach", "Plains Grotto", "Team Rocket's Castle"], 'Professor Kukui']}
    cur.execute('DROP TABLE IF EXISTS regions')
    cur.execute('CREATE TABLE regions (name TEXT, gen TEXT, towns TEXT, landmarks TEXT, professor TEXT)')
    for i in regions.keys():
        cur.execute('INSERT INTO regions (name, gen, towns, landmarks, professor) VALUES (?, ?, ?, ?, ?)', (regions[i][0], regions[i][1], json.dumps(regions[i][2]), json.dumps(regions[i][3]), regions[i][4]))
    print("Done")

def fillTowns():
    print("Starting towns table fill...")
    time.sleep(2)
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
             11 : ['New Bark Town', 'Johto', [], '2'],
             12 : ['Cherrygrove City', 'Johto', [], '2'],
             13 : ['Violet City', 'Johto', ['Falkner'], '2'],
             14 : ['Azalea Town', 'Johto', ['Bugsy'], '2'],
             15 : ['Goldenrod City', 'Johto', ['Whitney'], '2'],
             16 : ['Ecruteak City', 'Johto', ['Morty'], '2'],
             17 : ['Olivine City', 'Johto', ['Jasmine'], '2'],
             18 : ['Cianwood City', 'Johto', ['Chuck'], '2'],
             19 : ['Mahogany Town', 'Johto', ['Pryce'], '2'],
             20 : ['Blackthorn City', 'Johto', ['Clair'], '2'],
             21 : ['Littleroot Town', 'Hoenn', [], '3'],
             22 : ['Oldale Town', 'Hoenn', [], '3'],
             23 : ['Petalburg City', 'Hoenn', ['Norman'], '3'],
             24 : ['Rustboro City', 'Hoenn', ['Roxanne'], '3'],
             25 : ['Dewford Town', 'Hoenn', ['Brawly'], '3'],
             26 : ['Slateport City', 'Hoenn', [], '3'],
             27 : ['Mauville City', 'Hoenn', ['Wattson'], '3'],
             28 : ['Verdanturf Town', 'Hoenn', [], '3'],
             29 : ['Fallarbor Town', 'Hoenn', [], '3'],
             30 : ['Lavaridge Town', 'Hoenn', ['Flannery'], '3'],
             31 : ['Fortree City', 'Hoenn', ['Winona'], '3'],
             32 : ['Lilycove City', 'Hoenn', [], '3'],
             33 : ['Mossdeep City', 'Hoenn', ['Tate and Liza'], '3'],
             34 : ['Sootopolis City', 'Hoenn', ['Wallace', 'Juan'], '3'],
             35 : ['Pacifidlog Town', 'Hoenn', [], '3'],
             36 : ['Ever Grande City', 'Hoenn', [], '3'],
             37 : ['Twinleaf Town', 'Sinnoh', [], '4'],
             38 : ['Sandgem Town', 'Sinnoh', [], '4'],
             39 : ['Jubilife City', 'Sinnoh', [], '4'],
             40 : ['Oreburgh City', 'Sinnoh', ['Roark'], '4'],
             41 : ['Floaroma Town', 'Sinnoh', [], '4'],
             42 : ['Eterna City', 'Sinnoh', ['Gardenia'], '4'],
             43 : ['Hearthome City', 'Sinnoh', ['Fantina'], '4'],
             44 : ['Solaceon Town', 'Sinnoh', [], '4'],
             45 : ['Veilstone City', 'Sinnoh', ['Maylene'], '4'],
             46 : ['Pastoria City', 'Sinnoh', ['Crasher Wake'], '4'],
             47 : ['Celestic Town', 'Sinnoh', [], '4'],
             48 : ['Canalave City', 'Sinnoh', ['Byron'], '4'],
             49 : ['Snowpoint City', 'Sinnoh', ['Candice'], '4'],
             50 : ['Sunyshore City', 'Sinnoh', ['Volkner'], '4'],
             51 : ['Accumula Town', 'Unova', [], '5'],
             52 : ['Anville Town', 'Unova', [], '5'],
             53 : ['Aspertia City', 'Unova', ['Cheren'], '5'],
             54 : ['Black City', 'Unova', [], '5'],
             55 : ['Castelia City', 'Unova', ['Burgh'], '5'],
             56 : ['Driftveil City', 'Unova', ['Clay'], '5'],
             57 : ['Floccesy Town', 'Unova', [], '5'],
             58 : ['Humilau City', 'Unova', ['Marlon'], '5'],
             59 : ['Icirrus City', 'Unova', ['Brycen'], '5'],
             60 : ['Lacunosa Town', 'Unova', [], '5'],
             61 : ['Lentimas Town', 'Unova', [], '5'],
             62 : ['Mistralton City', 'Unova', ['Skyla'], '5'],
             63 : ['Nacrene City', 'Unova', ['Lenora'], '5'],
             64 : ['Nimbasa City', 'Unova', ['Elesa'], '5'],
             65 : ['Nuvema Town', 'Unova', [], '5'],
             66 : ['Opelucid City', 'Unova', ['Drayden', 'Iris'], '5'],
             67 : ['Striaton City', 'Unova', ['Cilan', 'Chili', 'Cress'], '5'],
             68 : ['Undella Town', 'Unova', [], '5'],
             69 : ['Virbank City', 'Unova', ['Roxie'], '5'],
             70 : ['White Forest', 'Unova', [], '5'],
             71 : ['Ambrette Town', 'Kalos', [], '6'],
             72 : ['Anistar City', 'Kalos', ['Olympia'], '6'],
             73 : ['Aquacorde Town', 'Kalos', [], '6'],
             74 : ['Camphrier Town', 'Kalos', [], '6'],
             75 : ['Coumarine City', 'Kalos', ['Ramos'], '6'],
             76 : ['Couriway Town', 'Kalos', [], '6'],
             77 : ['Cyllage City', 'Kalos', ['Grant'], '6'],
             78 : ['Dendemille Town', 'Kalos', [], '6'],
             79 : ['Geosenge Town', 'Kalos', [], '6'],
             80 : ['Kiloude City', 'Kalos', [], '6'],
             81 : ['Laverre City', 'Kalos', ['Valerie'], '6'],
             82 : ['Lumiose City', 'Kalos', ['Clemont'], '6'],
             83 : ['Santalune City', 'Kalos', ['Viola'], '6'],
             84 : ['Shalour City', 'Kalos', ['Korrina'], '6'],
             85 : ['Snowbelle City', 'Kalos', ['Wulfric'], '6'],
             86 : ['Vaniville Town', 'Kalos', [], '6'],
             87 : ["Hau'oli City", 'Alola', [], '7'],
             88 : ["Heahea City", 'Alola', [], '7'],
             89 : ["Iki Town", 'Alola', [], '7'],
             90 : ["Konikoni City", 'Alola', [], '7'],
             91 : ["Malie City", 'Alola', [], '7'],
             92 : ["Paniola Town", 'Alola', [], '7'],
             93 : ["Po Town", 'Alola', [], '7'],
             94 : ["Seafolk Village", 'Alola', [], '7'],
             95 : ["Tapu Village", 'Alola', [], '7']
             }
    cur.execute('DROP TABLE IF EXISTS towns')
    cur.execute('CREATE TABLE towns (name TEXT, region TEXT, leaders TEXT, gen TEXT)')
    for i in towns.keys():
        cur.execute('INSERT INTO towns (name, region, leaders, gen) VALUES (?, ?, ?, ?)', (towns[i][0], towns[i][1], json.dumps(towns[i][2]), towns[i][3]))
    print("Done")

def fillLeaders():
    print("Starting leaders table fill...")
    time.sleep(2)
    leaders = {1 : ['Brock', 'Pewter City', 'Rock', 'Boulder Badge', '1'],
               2 : ['Misty', 'Cerulean City', 'Water', 'Cascade Badge', '1'],
               3 : ['Lt. Surge', 'Vermilion City', 'Electric', 'Thunder Badge', '1'],
               4 : ['Erika', 'Celadon City', 'Grass', 'Rainbow Badge', '1'],
               5 : ['Koga', 'Fuchsia City', 'Poison', 'Soul Badge', '1'],
               6 : ['Sabrina', 'Saffron City', 'Psychic', 'Marsh Badge', '1'],
               7 : ['Blaine', 'Cinnabar Island', 'Fire', 'Volcano Badge', '1'],
               8 : ['Janine', 'Fuchsia City', 'Poison', 'Soul Badge', '2'],
               9 : ['Blue', 'Viridian City', '', 'Earth Badge', '2'],
               10 : ['Falkner', 'Violet City', 'Flying', 'Zephyr Badge', '2'],
               11 : ['Bugsy', 'Azalea Town', 'Bug', 'Hive Badge', '2'],
               12 : ['Whitney', 'Goldenrod City', 'Normal', 'Plain Badge', '2'],
               13 : ['Morty', 'Ecruteak City', 'Ghost', 'Fog Badge', '2'],
               14 : ['Jasmine', 'Olivine City', 'Steel', 'Mineral Badge', '2'],
               15 : ['Chuck', 'Cianwood City', 'Fighting', 'Storm Badge', '2'],
               16 : ['Pryce', 'Mahogany Town', 'Ice', 'Glacier Badge', '2'],
               17 : ['Clair', 'Blackthorn City', 'Dragon', 'Rising Badge', '2'],
               18 : ['Roxanne', 'Rustboro City', 'Rock', 'Stone Badge', '3'],
               19 : ['Brawly', 'Dewford Town', 'Fighting', 'Knuckle Badge', '3'],
               20 : ['Wattson', 'Mauville City', 'Electric', 'Dynamo Badge', '3'],
               21 : ['Flannery', 'Lavaridge Town', 'Fire', 'Heat Badge', '3'],
               22 : ['Norman', 'Petalburg City', 'Normal', 'Balance Badge', '3'],
               23 : ['Winona', 'Fortree City', 'Flying', 'Feather Badge', '3'],
               24 : ['Tate and Liza', 'Mossdeep City', 'Psychic', 'Mind Badge', '3'],
               25 : ['Wallace', 'Sootopolis City', 'Water', 'Rain Badge', '3'],
               26 : ['Juan', 'Sootopolis City', 'Water', 'Rain Badge', '3'],
               27 : ['Roark', 'Oreburgh City', 'Rock', 'Coal Badge', '4'],
               28 : ['Gardenia', 'Eterna City', 'Grass', 'Forest Badge', '4'],
               29 : ['Maylene', 'Veilstone City', 'Fighting', 'Cobble Badge', '4'],
               30 : ['Crasher Wake', 'Pastoria City', 'Water', 'Fen Badge', '4'],
               31 : ['Fantina', 'Hearthome City', 'Ghost', 'Relic Badge', '4'],
               32 : ['Byron', 'Canalave City', 'Steel', 'Mine Badge', '4'],
               33 : ['Candice', 'Snowpoint City', 'Ice', 'Icicle Badge', '4'],
               34 : ['Volkner', 'Sunyshore City', 'Electric', 'Beacon Badge', '4'],
               35 : ['Cilan', 'Striaton City', 'Grass', 'Trio Badge', '5'],
               36 : ['Chili', 'Striaton City', 'Fire', 'Trio Badge', '5'],
               37 : ['Cress', 'Striaton City', 'Water', 'Trio Badge', '5'],
               38 : ['Lenora', 'Nacrene City', 'Normal', 'Basic Badge', '5'],
               39 : ['Burgh', 'Castelia City', 'Bug', 'Insect Badge', '5'],
               40 : ['Elesa', 'Nimbasa City', 'Electic', 'Bolt Badge', '5'],
               41 : ['Clay', 'Driftveil City', 'Ground', 'Quake Badge', '5'],
               42 : ['Skyla', 'Mistralton City', 'Flying', 'Jet Badge', '5'],
               43 : ['Brycen', 'Icirrus City', 'Ice', 'Freeze Badge', '5'],
               44 : ['Drayden', 'Opelucid City', 'Dragon', 'Legend Badge', '5'],
               45 : ['Iris', 'Opelucid City', 'Dragon', 'Legend Badge', '5'],
               46 : ['Cheren', 'Aspertia City', 'Normal', 'Basic Badge', '5'],
               47 : ['Roxie', 'Virbank City', 'Poison', 'Toxic Badge', '5'],
               48 : ['Marlon', 'Humilau City', 'Water', 'Wave Badge', '5'],
               49 : ['Viola', 'Santalune City', 'Bug', 'Bug Badge', '6'],
               50 : ['Grant', 'Cyllage City', 'Rock', 'Cliff Badge', '6'],
               51 : ['Korrina', 'Shalour City', 'Fighting', 'Rumble Badge', '6'],
               52 : ['Ramos', 'Coumarine City', 'Grass', 'Plant Badge', '6'],
               53 : ['Clemont', 'Lumiose City', 'Electric', 'Voltage Badge', '6'],
               54 : ['Valerie', 'Laverre City', 'Fairy', 'Fairy Badge', '6'],
               55 : ['Olympia', 'Anistar City', 'Psychic', 'Psychic Badge', '6'],
               56 : ['Wulfric', 'Snowbelle City', 'Ice', 'Iceberg Badge', '6']
    }
    cur.execute('DROP TABLE IF EXISTS leaders')
    cur.execute('CREATE TABLE leaders (name TEXT, town TEXT, specialty TEXT, badge TEXT, gen TEXT)')
    for i in leaders.keys():
        cur.execute('INSERT INTO leaders (name, town, specialty, badge, gen) VALUES (?, ?, ?, ?, ?)', (leaders[i][0], leaders[i][1], leaders[i][2], leaders[i][3], leaders[i][4]))
    print("Done")


# Start database population / API scraping
# Open connection to sqlite file
db = 'pokequiz.sqlite'
conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES) # auto-detect and convert types
cur = conn.cursor()

# Uncomment functions below to fill corresponding tables

#fillTeams()
#fillGames()
#fillRegions()
#fillTowns()
#fillLeaders()
#fillPokemon()

#cur.execute('SELECT * FROM pokemon ORDER BY RANDOM() LIMIT 5;')
#for row in cur:
    #print(row)
    #print(type(row[1]))


# Commit additions and close connection
conn.commit()

#test stuff
#cur.execute('SELECT * FROM pokemon ORDER BY RANDOM() LIMIT 5;')
#for row in cur:
    #print(row)
    #print(row[0])
    #print(type(row[0]))
    #print(row[3])
    #print(json.loads(row[2]))
    #print(type(json.loads(row[2])))

# Close connection to db
conn.close()
