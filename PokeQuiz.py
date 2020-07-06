import random
import sqlite3
from Classes import *

# TODO create reference chart somewhere with question categories (RegionQuestion, PokemonQuestion, etc.) and their types (1, 2, etc.)
def getQuestion():
    # Question selection
    categories = 6 # (Pokemon, Leader, Town, Team, Region, Game)
    # selection = random.randint(1, categories)
    selection = 4 #team question

    # PokemonQuestion
    if selection == 1:
        question = PokemonQuestion()
        pokemon = randomPokemon()
        # "What is the evolution of {}?"
        if question.type == 1:
            pass # do thing for pokemon question type 1
        # "In what generation was {} introduced?"
        elif question.type == 2:
            question.Q = question.Q.format(pokemon.name)
            question.A = pokemon.gen_introduced

    # LeaderQuestion
    elif selection == 2:
        question = LeaderQuestion()
        leader = randomLeader()
        # "What is the name of the Gym Leader of {}?"
        if question.type == 1:
            question.Q = question.Q.format(leader.town)
            question.A = leader.name
        # "What is the name of the town where Gym Leader {}'s Gym is?"
        elif question.type == 2:
            question.Q = question.Q.format(leader.name)
            question.A = leader.town
        # "What is the Type specialty of Gym Leader {}?"
        elif question.type == 3:
            question.Q = question.Q.format(leader.name)
            question.A = leader.specialty
        # "What is the name of the Badge of Gym Leader {}?"
        elif question.type == 4:
            question.Q = question.Q.format(leader.name)
            question.A = leader.badge

    # TownQuestion
    elif selection == 3:
        question = TownQuestion()
        town = randomTown()
        # "What region is {} in?"
        if question.type == 1:
            question.Q = question.Q.format(town.name)
            question.A = town.region

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
        return question

    # RegionQuestion
    elif selection == 5:
        question = RegionQuestion()
        region = randomRegion()
        # "{} is located in what region?"
        if question.type == 1:
            question.Q = question.Q.format(region.landmarks) # change this to be ONE random landmark from landmarks list
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
            question.Q = question.Q.format(region.towns) # change this to be ONE random town from towns list
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
            question.A = game.rivals # change this to be ONE random rival from rivals list




def randomPokemon():
    """Creates and returns a random Pokemon object."""
    return

def randomLeader():
    """Creates and returns a random Leader object."""
    return

def randomTeam():
    """Creates and returns a random Team object."""
    conn = sqlite3.connect('pokequiz.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM teams ORDER BY RANDOM() LIMIT 1;')
    for row in cur:
        sel = row
    conn.close()
    return Team(*sel)

def randomTown():
    """Creates and returns a random Town object."""
    return

def randomRegion():
    """Creates and returns a random Region object."""
    return

def randomGame():
    """Creates and returns a random Game object."""
    return

# Start
print("Welcome to PokeQuiz!")
# geodude = Pokemon("Geodude", False, ["Graveler"], "1") # test
q = getQuestion()
print(q.Q)
print(q.A)
