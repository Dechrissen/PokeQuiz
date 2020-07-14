import random
import sqlite3
from Classes import *
from Functions import getQuestion, answerCheck


# Settings
limit = 2 # Question limit
score = 0
excluded = [] # Excluded gens
status = True # Continue status

def mainMenu():
    global limit
    global score
    global excluded
    global status
    print("Please select an option below:\n")
    print("1 - Quick Study")
    print("2 - Marathon Mode")
    print("3 - Study Individual Categories")
    print("4 - Options")
    print("5 - Quit\n")
    user_input = input("> ")
    if user_input == '1':
        return
    else:
        print("Goodbye!")
        quit()

def individualCategories():
    pass

def options():
    pass

# Start
print("- Welcome to PokeQuiz! -\n")
mainMenu()
while status is True:
    for i in range(limit):
        question = getQuestion()
        user_input = input(question.Q + " ")
        result = answerCheck(question, user_input)
        if result:
            print("Incorrect! Correct answer is:", result)
        else:
            print("Correct!")

    # Ask user if they want to study again
    user_input = input("Would you like to study again? ")
    if user_input == "yes":
        continue
    else:
        status = False
print("Goodbye!")
