import random
import sqlite3
from Classes import *
from Functions import getQuestion, answerCheck



# Start
print("Welcome to PokeQuiz!")
question = getQuestion()
input = input(question.Q + " ")
result = answerCheck(question, input)
if result:
    print("Incorrect! Correct answer is:", result)
else:
    print("Correct!")
