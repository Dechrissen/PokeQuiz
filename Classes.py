import random

class Game:
    """Class for Pokémon games."""

    def __init__(self, name, region, gen, team, champion):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Game name must be string')
        if type(region) is not str:
            raise TypeError('Region must be string')
        if type(gen) is not str:
            raise TypeError('Gen must be string')
        if type(team) is not str:
            raise TypeError('Team must be string')
        if type(champion) is not str:
            raise TypeError('Champion must be string')

        # Initialize object variables
        self.name = name
        self.region = region
        self.gen = gen
        self.team = team
        self.champion = champion

class Region:
    """Class for regions in the Pokémon world."""

    def __init__(self, name, gen, towns, rival, landmarks, professor):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Region name must be string')
        if type(gen) is not str:
            raise TypeError('Gen must be string')
        if type(towns) is not list:
            raise TypeError('towns must be list')
        for town in towns:
            if type(town) is not str:
                raise TypeError('Town names must be strings')
        if type(rival) is not str:
            raise TypeError('Rival name must be string')
        if type(landmarks) is not list:
            raise TypeError('landmarks must be list')
        for landmark in landmarks:
            if type(landmark) is not str:
                raise TypeError('Landmark names must be strings')
        if type(professor) is not str:
            raise TypeError('Professor name must be string')

        # Initialize object variables
        self.name = name
        self.gen = gen
        self.towns = towns
        self.rival = rival
        self.landmarks = landmarks
        self.professor = professor

class Town:
    """Class for towns in the Pokémon world."""

    def __init__(self, name, region, leader):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Town name must be string')
        if type(region) is not str:
            raise TypeError('Region must be string')
        if type(leader) is not str:
            raise TypeError('Leader must be string')

        # Initialize object variables
        self.name = name
        self.region = region
        self.leader = leader

class Leader:
    """Class for Gym Leaders in the Pokémon world."""

    def __init__(self, name, town, specialty, badge):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Leader name must be string')
        if type(town) is not str:
            raise TypeError('Town must be string')
        if type(specialty) is not str:
            raise TypeError('Type specialty must be string')
        if type(badge) is not str:
            raise TypeError('Badge name must be string')

        # Initialize object variables
        self.name = name
        self.town = town
        self.specialty = specialty
        self.badge = badge

class Pokemon:
    """Class for Pokémon."""

    def __init__(self, name, final_stage, evolution, gen_introduced):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Leader name must be string')
        if type(final_stage) is not bool:
            raise TypeError('Final stage must be boolean')
        if type(evolution) is not list and evolution is not None:
            raise TypeError('Evolution must be list or None')
        for evo in evolution:
            if type(evo) is not str:
                raise TypeError('Evolutions must be strings')
        if type(gen_introduced) is not str:
            raise TypeError('Gen introduced must be string')

        # Initialize object variables
        self.name = name
        self.final_stage = final_stage
        self.evolution = evolution
        self.gen_introduced = gen_introduced

class LeaderQuestion:
    """Class for Gym Leader questions."""

    def __init__(self):
        types = {1 : "What is the name of the Gym Leader of {}?",
                 2 : "What is the name of the town where Gym Leader {}'s Gym is?",
                 3 : "What is the Type specialty of Gym Leader {}?",
                 4 : "What is the name of the Badge of Gym Leader {}?"}
        n = random.randint(range(len(types)))

        # Initialize object variables
        self.type =  n
        self.Q = types[n]
        self.A = None

class TownQuestion:
    """Class for Town questions."""

    def __init__(self):
        types = {1 : "What region is {} in?"}
        n = random.randint(range(len(types)))

        # Initialize object variables
        self.type = n
        self.Q = types[n]
        self.A = None

class PokemonQuestion:
    """Class for Pokemon questions."""

    def __init__(self):
        types = {1 : "What is the evolution of {}?",
                 2 : "In what generation was {} introduced?"}
        n = random.randint(range(len(types)))

        # Initialize object variables
        self.type = n
        self.Q = types[n]
        self.A = None

class TeamQuestion:
    """Class for Team questions."""

    def __init__(self):
        types = {1 : "{} is the enemy team in what region?",
                 2 : "The leader of {} is who?",
                 3 : "{} is the leader of what enemy team?"}
        n = random.randint(range(len(types)))

        # Initialize object variables
        self.type = n
        self.Q = types[n]
        self.A = None
