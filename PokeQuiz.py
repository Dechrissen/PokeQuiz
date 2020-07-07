import random
import sqlite3
from Classes import *
from Functions import *

# Database
db = 'pokequiz.sqlite'

# Pokemon which are among the branched evolutions
branches = ['vileplume', 'bellossom', 'poliwrath', 'politoed', 'slowbro', 'slowking', 'vaporeon', 'jolteon', 'flareon', 'espeon', 'umbreon',
            'leafeon', 'glaceon', 'sylveon', 'hitmonlee', 'hitmonchan', 'hitmontop', 'silcoon', 'cascoon', 'gardevoir', 'gallade', 'ninjask',
            'shedinja', 'glalie', 'froslass', 'huntail', 'gorebyss', 'wormadam', 'mothim', 'solgaleo', 'lunala', 'flapple', 'appletun']

# Start
print("Welcome to PokeQuiz!")
q = getQuestion()
print(q.Q)
print(q.A)
