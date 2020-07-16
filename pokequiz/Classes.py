import random

class Game:
    """Class for Pokémon games."""

    def __init__(self, name, region, gen, rivals, champion):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Game name must be string')
        if type(region) is not str:
            raise TypeError('Region must be string')
        if type(gen) is not str:
            raise TypeError('Gen must be string')
        if type(rivals) is not list:
            raise TypeError('rivals must be list')
        if type(champion) is not str:
            raise TypeError('Champion must be string')

        # Initialize object variables
        self.name = name
        self.region = region
        self.gen = gen
        self.rivals = rivals
        self.champion = champion

class Region:
    """Class for regions in the Pokémon world."""

    def __init__(self, name, gen, towns, landmarks, professor):
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
        self.landmarks = landmarks
        self.professor = professor

class Town:
    """Class for towns in the Pokémon world."""

    def __init__(self, name, region, leaders, gen):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Town name must be string')
        if type(region) is not str:
            raise TypeError('Region must be string')
        if type(leaders) is not list:
            raise TypeError('Leaders must be list')
        if type(gen) is not str:
            raise TypeError('Gen must be string')

        # Initialize object variables
        self.name = name
        self.region = region
        self.leaders = leaders
        self.gen = gen

class Leader:
    """Class for Gym Leaders in the Pokémon world."""

    def __init__(self, name, town, specialty, badge, gen):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Leader name must be string')
        if type(town) is not str:
            raise TypeError('Town must be string')
        if type(specialty) is not str:
            raise TypeError('Type specialty must be string')
        if type(badge) is not str:
            raise TypeError('Badge name must be string')
        if type(gen) is not str:
            raise TypeError('Gen must be string')

        # Initialize object variables
        self.name = name
        self.town = town
        self.specialty = specialty
        self.badge = badge
        self.gen = gen

class Team:
    """Class for Teams of the Pokémon world."""

    def __init__(self, name, boss, region, gen):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Team name must be string')
        if type(boss) is not str:
            raise TypeError('Boss name must be string')
        if type(region) is not str:
            raise TypeError('Region name must be string')
        if type(gen) is not str:
            raise TypeError('Gen must be string')

        # Initialize object variables
        self.name = name
        self.boss = boss
        self.region = region
        self.gen = gen


class Pokemon:
    """Class for Pokémon."""

    def __init__(self, name, preevo, types, gen):
        # Validate given parameters
        if type(name) is not str:
            raise TypeError('Leader name must be string')
        if type(preevo) is not str and preevo is not None:
            raise TypeError('Pre-evolution must be str or None')
        if type(types) is not list:
            raise TypeError('types must be list')
        if type(gen) is not str:
            raise TypeError('Gen must be string')

        # Initialize object variables
        self.name = name
        self.preevo = preevo
        self.types = types
        self.gen = gen

class LeaderQuestion:
    """Class for Gym Leader questions."""

    def __init__(self):
        types = {1 : "In what town is {}'s Gym located?",
                 2 : "What is the Type specialty of Gym Leader {}?",
                 3 : "What is the name of the Badge of Gym Leader {}?"}
        n = random.randint(1, len(types.keys()))

        # Initialize object variables
        self.type =  n
        self.Q = types[n]
        self.A = None

class TownQuestion:
    """Class for Town questions."""

    def __init__(self):
        types = {1 : "In what region is {} located?",
                 2 : "What is the name of the Gym Leader of {}?"}
        n = random.randint(1, len(types.keys()))

        # Initialize object variables
        self.type = n
        self.Q = types[n]
        self.A = None

class PokemonQuestion:
    """Class for Pokemon questions."""

    def __init__(self):
        types = {1 : "What is the evolution of {}?",
                 2 : "In what generation was {} introduced?",
                 3 : "What evolves into {}?",
                 4 : "What is {}'s type? (space separated if there are two)"}
        n = random.randint(1, len(types.keys()))

        # Initialize object variables
        self.type = n
        self.Q = types[n]
        self.A = None

class TeamQuestion:
    """Class for Team questions."""

    def __init__(self):
        types = {1 : "{} is the enemy team in what region?",
                 2 : "Who is the boss of {}?",
                 3 : "{} is the boss of what enemy team?"}
        n = random.randint(1, len(types.keys()))

        # Initialize object variables
        self.type = n
        self.Q = types[n]
        self.A = None

class RegionQuestion:
    """Class for Region questions."""

    def __init__(self):
        types = {1 : "{} is a landmark in what region?",
                 2 : "Who is the professor in {}?",
                 3 : "In what generation was {} introduced?",
                 4 : "{} is a town in what region?"}
        n = random.randint(1, len(types.keys()))

        # Initialize object variables
        self.type = n
        self.Q = types[n]
        self.A = None

class GameQuestion:
    """Class for Game questions."""

    def __init__(self):
        types = {1 : "Who is the Champion in {} version?",
                 2 : "Who is a rival in {} version?"}
        n = random.randint(1, len(types.keys()))

        # Initialize object variables
        self.type = n
        self.Q = types[n]
        self.A = None

class seedQuestion:
    def __init__(self, Q, A):
        self.Q = Q
        self.A = A
