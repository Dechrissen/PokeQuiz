import random

def getQuestion():
    # Question selection
    categories = 4 # (Pokemon, Leader, Town, Team)
    selection = random.randint(1, categories)
    question = None

    # PokemonQuestion
    if selection == 1:
        question = PokemonQuestion()
        # "What is the evolution of {}?"
        if question.type == 1:
            pass # do thing for pokemon question type 1
        # "In what generation was {} introduced?"
        elif question.type == 2:
            pokemon = Pokemon("geodude", False, ["Graveler"], "1") # replace with randomPokemon()
            question.Q = question.Q.format(pokemon.name)
            question.A = pokemon.gen_introduced

    # LeaderQuestion
    elif selection == 2:
        question = LeaderQuestion()
        # "What is the name of the Gym Leader of {}?"
        if question.type == 1:
            leader = randomLeader()
            question.Q = question.Q.format(leader.town)
            question.A = leader.name
        # "What is the name of the town where Gym Leader {}'s Gym is?"
        elif question.type == 2:
            leader = randomLeader()
            question.Q = question.Q.format(leader.name)
            question.A = leader.town
        # "What is the Type specialty of Gym Leader {}?"
        elif question.type == 3:
            leader = randomLeader()
            question.Q = question.Q.format(leader.name)
            question.A = leader.specialty
        # "What is the name of the Badge of Gym Leader {}?"
        elif question.type == 4:
            leader = randomLeader()
            question.Q = question.Q.format(leader.name)
            question.A = leader.badge

    # TownQuestion
    elif selection == 3:
        question = TownQuestion()
        # "What region is {} in?"
        if question.type == 1:
            town = randomTown()
            question.Q = question.Q.format(town.name)
            question.A = town.region

    # TeamQuestion -- do I use a Team object or something simpler?
    elif selection == 4:
        question = TeamQuestion()
        if question.type == 1:
            pass # do thing for type 1
        elif question.type == 2:
            pass # do thing for type 2
        elif question.type == 3:
            pass # do thing for type 3

def randomPokemon():
    """Creates and returns a random Pokemon object."""
    return

def randomLeader():
    """Creates and returns a random Leader object."""
    return

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
geodude = Pokemon("geodude", False, ["Graveler"], "1") # test







# TODO create reference chart somewhere with question categories (RegionQuestion, PokemonQuestion, etc.) and their subtypes (1, 2, etc.)
