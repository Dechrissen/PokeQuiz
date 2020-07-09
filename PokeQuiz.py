import random
import sqlite3
from Classes import *
from Functions import *

# Database
db = 'pokequiz.sqlite'

# Start
print("Welcome to PokeQuiz!")
q = getQuestion()
print(q.Q)
print(q.A)
