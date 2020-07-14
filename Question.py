from Classes import *
import sqlite3
import json
import random


def getQuestion(choice, excluded):
    # Question selection
    # 1-Pokemon, 2-Leader, 3-Town, 4-Team, 5-Region, 6-Game
    selection = random.randint(1, 6)
    # Check if choice was supplied, and if so, overwrite selection
    if choice:
        selection = choice
    # Pokemon which are among the branched evolutions
    branches = ['Vileplume', 'Bellossom', 'Poliwrath', 'Politoed', 'Slowbro', 'Slowking', 'Vaporeon', 'Jolteon', 'Flareon', 'Espeon', 'Umbreon',
                'Leafeon', 'Glaceon', 'Sylveon', 'Hitmonlee', 'Hitmonchan', 'Hitmontop', 'Silcoon', 'Cascoon', 'Gardevoir', 'Gallade', 'Ninjask',
                'Shedinja', 'Glalie', 'Froslass', 'Huntail', 'Gorebyss', 'Wormadam', 'Mothim', 'Solgaleo', 'Lunala', 'Flapple', 'Appletun']

    # PokemonQuestion
    if selection == 1:
        question = PokemonQuestion()
        pokemon = randomPokemon()
        while pokemon.gen in excluded:
            pokemon = randomPokemon()
        # "What is the evolution of {}?"
        if question.type == 1:
            # Do not ask this question while the Pokemon is from a branched evolution line, or while Pokemon has no preevo
            while (pokemon.name in branches) or (pokemon.preevo is None) or (pokemon.gen in excluded):
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
            while (pokemon.preevo is None) or (pokemon.gen in excluded):
                pokemon = randomPokemon()
            question.Q = question.Q.format(pokemon.name)
            question.A = pokemon.preevo
        # "What is {}'s type? (space separated if there are two)"
        elif question.type == 4:
            question.Q = question.Q.format(pokemon.name)
            question.A = pokemon.types # List, special case

    # LeaderQuestion
    elif selection == 2:
        question = LeaderQuestion()
        leader = randomLeader()
        while leader.gen in excluded:
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
        while town.gen in excluded:
            town = randomTown()
        # "In what region is {} located?"
        if question.type == 1:
            question.Q = question.Q.format(town.name)
            question.A = town.region
        # "What is the name of the Gym Leader of {}?"
        elif question.type == 2:
            while (len(town.leaders) == 0) or (town.gen in excluded):
                town = randomTown()
            question.Q = question.Q.format(town.name)
            question.A = town.leaders # List

    # TeamQuestion
    elif selection == 4:
        question = TeamQuestion()
        team = randomTeam()
        while team.gen in excluded:
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
        while region.gen in excluded:
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
        while game.gen in excluded:
            game = randomGame()
        # "Who is the Champion in {}?"
        if question.type == 1:
            question.Q = question.Q.format(game.name)
            question.A = game.champion
        # "Who is a rival in {}?"
        elif question.type == 2:
            question.Q = question.Q.format(game.name)
            question.A = game.rivals # List
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

def removeWords(answer):
    words = [' town', ' city', ' island', ' badge', 'professor ', 'team ']
    answer = answer.lower()
    for word in words:
        answer = answer.replace(word, '')
    return answer

def answerCheck(question, input):
    # this function should first check the type of the answer,
    # whether it's str or list, then check if the input is
    # equal to the answer (if str) or in the answer (if list)
    # returns tuple  of bool (right or wrong) and correction
    # if needed, None otherwise
    result = None
    # First and foremost, check if input == "quit" to exit program
    if input.lower().strip() == 'quit':
        print("Goodbye!")
        quit()
    # First do a check for the question "What type is {X Pokemon}?" because it's a special case
    elif type(question) is PokemonQuestion and question.type == 4:
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

    # Then check for string answers
    elif type(question.A) is str:
        # Clean input to remove 'town', 'city', 'badge', etc.
        input = removeWords(input)
        input = input.replace(' ', '').strip().lower()
        answer = removeWords(question.A)
        answer = answer.replace(' ', '').strip().lower()
        if input == answer:
            result = None
        else:
            result = question.A

    # Finally check for list answers
    elif type(question.A) is list:
        input = input.replace(' ', '').strip().lower()
        answer = [x.replace(' ', '').strip().lower() for x in question.A]
        if input in answer:
            result = None
        else:
            result = ' or '.join(question.A)
    return result
