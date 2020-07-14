from Classes import *
import sqlite3
import json
import random


def getQuestion():
    # Question selection
    categories = 6 # (Pokemon, Leader, Town, Team, Region, Game)
    selection = random.randint(1, categories)
    #selection = 2
    # Pokemon which are among the branched evolutions
    branches = ['Vileplume', 'Bellossom', 'Poliwrath', 'Politoed', 'Slowbro', 'Slowking', 'Vaporeon', 'Jolteon', 'Flareon', 'Espeon', 'Umbreon',
                'Leafeon', 'Glaceon', 'Sylveon', 'Hitmonlee', 'Hitmonchan', 'Hitmontop', 'Silcoon', 'Cascoon', 'Gardevoir', 'Gallade', 'Ninjask',
                'Shedinja', 'Glalie', 'Froslass', 'Huntail', 'Gorebyss', 'Wormadam', 'Mothim', 'Solgaleo', 'Lunala', 'Flapple', 'Appletun']

    # PokemonQuestion
    if selection == 1:
        question = PokemonQuestion()
        pokemon = randomPokemon()
        # "What is the evolution of {}?"
        if question.type == 1:
            # Do not ask this question while the Pokemon is from a branched evolution line, or while Pokemon has no preevo
            while (pokemon.name in branches) or (pokemon.preevo is None):
                pokemon = randomPokemon()
            question.Q = question.Q.format(pokemon.preevo)
            question.A = pokemon.name
        # "In what generation was {} introduced?"
        elif question.type == 2:
            question.Q = question.Q.format(pokemon.name)
            question.A = pokemon.gen
        # "What evolves into {}?"
        elif question.type == 3:
            # Do not ask this question while Pokemon has no preevo
            while (pokemon.preevo is None):
                pokemon = randomPokemon()
            question.Q = question.Q.format(pokemon.name)
            question.A = pokemon.preevo
        # "What is {}'s type? (space separated if there are two)"
        elif question.type == 4:
            question.Q = question.Q.format(pokemon.name)
            question.A = pokemon.types

    # LeaderQuestion
    elif selection == 2:
        question = LeaderQuestion()
        leader = randomLeader()
        # "In what town is {}'s Gym located?""
        if question.type == 1:
            question.Q = question.Q.format(leader.name)
            question.A = leader.town
        # "What is the Type specialty of Gym Leader {}?"
        elif question.type == 2:
            question.Q = question.Q.format(leader.name)
            question.A = leader.specialty
        # "What is the name of the Badge of Gym Leader {}?"
        elif question.type == 3:
            question.Q = question.Q.format(leader.name)
            question.A = leader.badge

    # TownQuestion
    elif selection == 3:
        question = TownQuestion()
        town = randomTown()
        # "In what region is {} located?"
        if question.type == 1:
            question.Q = question.Q.format(town.name)
            question.A = town.region
        # "What is the name of the Gym Leader of {}?"
        elif question.type == 2:
            while (len(town.leaders) == 0):
                town = randomTown()
            question.Q = question.Q.format(town.name)
            question.A = town.leaders

    # TeamQuestion
    elif selection == 4:
        question = TeamQuestion()
        team = randomTeam()
        # "{} is the enemy team in what region?"
        if question.type == 1:
            question.Q = question.Q.format(team.name)
            question.A = team.region
        # "Who is the boss of {}?"
        elif question.type == 2:
            question.Q = question.Q.format(team.name)
            question.A = team.boss
        # "{} is the boss of what enemy team?"
        elif question.type == 3:
            question.Q = question.Q.format(team.boss)
            question.A = team.name

    # RegionQuestion
    elif selection == 5:
        question = RegionQuestion()
        region = randomRegion()
        # "{} is a landmark in what region?"
        if question.type == 1:
            random_landmark = random.choice(region.landmarks)
            question.Q = question.Q.format(random_landmark)
            question.A = region.name
        # "Who is the professor in {}?"
        elif question.type == 2:
            question.Q = question.Q.format(region.name)
            question.A = region.professor
        # "In what generation was {} introduced?"
        elif question.type == 3:
            question.Q = question.Q.format(region.name)
            question.A = region.gen
        # "{} is a town in what region?"
        elif question.type == 4:
            random_town = random.choice(region.towns)
            question.Q = question.Q.format(random_town)
            question.A = region.name

    # GameQuestion
    elif selection == 6:
        question = GameQuestion()
        game = randomGame()
        # "Who is the Champion in {}?"
        if question.type == 1:
            question.Q = question.Q.format(game.name)
            question.A = game.champion
        # "Who is a rival in {}?"
        elif question.type == 2:
            question.Q = question.Q.format(game.name)
            question.A = game.rivals
    return question

def randomPokemon():
    """Creates and returns a random Pokemon object."""
    # Database
    db = 'pokequiz.sqlite'

    # Establish connection to SQLite database
    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # Get random Pokemon
    cur.execute('SELECT * FROM pokemon ORDER BY RANDOM() LIMIT 1;')
    sel = list(cur.fetchone())
    # Parse types list
    sel[2] = json.loads(sel[2])

    # Close connection
    conn.close()

    return Pokemon(*sel)

def randomLeader():
    """Creates and returns a random Leader object."""
    # Database
    db = 'pokequiz.sqlite'

    # Establish connection to SQLite database
    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # Get random Gym Leader
    cur.execute('SELECT * FROM leaders ORDER BY RANDOM() LIMIT 1;')
    sel = cur.fetchone()

    # Close connection
    conn.close()

    return Leader(*sel)

def randomTeam():
    """Creates and returns a random Team object."""
    # Database
    db = 'pokequiz.sqlite'

    # Establish connection to SQLite database
    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # Get random Team
    cur.execute('SELECT * FROM teams ORDER BY RANDOM() LIMIT 1;')
    sel = cur.fetchone()

    # Close connection
    conn.close()

    return Team(*sel)

def randomTown():
    """Creates and returns a random Town object."""
    # Database
    db = 'pokequiz.sqlite'

    # Establish connection to SQLite database
    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # Get random Town
    cur.execute('SELECT * FROM towns ORDER BY RANDOM() LIMIT 1;')
    sel = list(cur.fetchone())
    # Parse leaders list
    sel[2] = json.loads(sel[2])

    # Close connection
    conn.close()

    return Town(*sel)

def randomRegion():
    """Creates and returns a random Region object."""
    # Database
    db = 'pokequiz.sqlite'

    # Establish connection to SQLite database
    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # Get random Region
    cur.execute('SELECT * FROM regions ORDER BY RANDOM() LIMIT 1;')
    sel = list(cur.fetchone())
    # Parse towns list
    sel[2] = json.loads(sel[2])
    # Parse landmarks list
    sel[3] = json.loads(sel[3])

    # Close connection
    conn.close()

    return Region(*sel)

def randomGame():
    """Creates and returns a random Game object."""
    # Database
    db = 'pokequiz.sqlite'

    # Establish connection to SQLite database
    conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # Get random Game
    cur.execute('SELECT * FROM games ORDER BY RANDOM() LIMIT 1;')
    sel = list(cur.fetchone())
    # Parse rivals list
    sel[3] = json.loads(sel[3])

    # Close connection
    conn.close()

    return Game(*sel)

def answerCheck(question, input):
    # this function should first check the type of the answer,
    # whether it's str or list, then check if the input is
    # equal to the answer (if str) or in the answer (if list)
    # returns tuple  of bool (right or wrong) and correction
    # if needed, None otherwise
    result = None

    # First do a check for the question "What type is {X Pokemon}?" because it's a special case
    if type(question) is PokemonQuestion and question.type == 4:
        # Check if nothing was entered
        if input == '':
            return ' '.join(question.A)
        answer = [x.lower() for x in question.A]
        input = input.lower().strip().split()
        # Check if more than 2 types were entered
        if len(input) > 2:
            return ' '.join(question.A)
        # Check if both types entered are the same (if 2 were entered)
        if len(input) == 2:
            if input[0] == input[1]:
                return ' '.join(question.A)
        # Now check for correctness
        for t in input:
            if t not in answer:
                return ' '.join(question.A)
        # Return None (correct) if all checks pass
        return None

    elif type(question.A) is str:
        input = input.replace(' ', '').strip().lower()
        x = question.A.replace(' ', '').strip().lower()
        if input == x:
            result = None
        else:
            result = question.A
    elif type(question.A) is list:
        input = input.replace(' ', '').strip().lower()
        answer = [x.replace(' ', '').strip().lower() for x in question.A]
        if input in answer:
            result = None
        else:
            result = ' or '.join(question.A)
    return result
