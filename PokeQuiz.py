import random
import sqlite3
from Classes import *
from Question import getQuestion, answerCheck
import time


# Settings
limit = 10 # Question limit
score = 0
excluded = [] # Excluded gens
status = True # Continue status
choice = None # Question type (None by default, because all are included)


def mainMenu():
    global limit
    print("Please select an option below:\n")
    print("1 - Start Quiz")
    print("2 - Study Individual Categories")
    print("3 - Marathon Mode")
    print("4 - Options")
    print("5 - Help")
    print("6 - Quit\n")
    user_input = input("> ").strip()
    if user_input == '1':
        return
    elif user_input == '2':
        individualCategories()
    elif user_input == '3':
        limit = 999
    elif user_input == '4':
        options()
    elif user_input == '5':
        print("This is where the help section will go...")
        mainMenu()
    else:
        print("Goodbye!")
        quit()

def individualCategories():
    global choice
    print("Please select an option below:\n")
    print("1 - Study Pokemon")
    print("2 - Study Games")
    print("3 - Study Regions")
    print("4 - Study Towns")
    print("5 - Study Gym Leaders")
    print("6 - Study Teams")
    print("7 - Back to Main Menu")
    print("8 - Quit\n")
    user_input = input("> ").strip()
    if user_input == '1':
        choice = 1
    elif user_input == '2':
        choice = 6
    elif user_input == '3':
        choice = 5
    elif user_input == '4':
        choice = 3
    elif user_input == '5':
        choice = 2
    elif user_input == '6':
        choice = 4
    elif user_input == '7':
        mainMenu()
    else:
        print("Goodbye!")
        quit()

def options():
    global limit
    global excluded
    print("Please select an option below:\n")
    print("1 - Filter Generations")
    print("2 - Set Question Limit")
    print("3 - Back to Main Menu")
    print("4 - Quit\n")
    user_input = input("> ").strip()
    if user_input == '1':
        print("Enter an upper limit for Generation to restrict questions: (1 - 7)")
        gen = input("> ").strip()
        if gen == '1':
            excluded = ['2','3','4','5','6','7']
            print("Generation 2 - 7 questions will be excluded.")
        elif gen == '2':
            excluded = ['3','4','5','6','7']
            print("Generation 3 - 7 questions will be excluded.")
        elif gen == '3':
            excluded = ['4','5','6','7']
            print("Generation 4 - 7 questions will be excluded.")
        elif gen == '4':
            excluded = ['5','6','7']
            print("Generation 5 - 7 questions will be excluded.")
        elif gen == '5':
            excluded = ['6','7']
            print("Generation 6 - 7 questions will be excluded.")
        elif gen == '6':
            excluded = ['7']
            print("Generation 7 questions will be excluded.")
        elif gen == '7':
            print("No Generations will be excluded.")
        else:
            print("Invalid input.")
        print("Returning to Options menu...\n")
        options()
    elif user_input == '2':
        print("Enter desired number of questions per quiz:")
        num = input("> ").strip()
        try:
            limit = int(num)
            print("Question limit set to", num, "\nReturning to Options menu...\n")
            options()
        except ValueError:
            print("Invalid input.\nReturning to Options menu...\n")
            options()
    elif user_input == '3':
        mainMenu()
    else:
        print("Goodbye!")
        quit()


# Start
print("--------------------\nWelcome to PokeQuiz!\n--------------------\n")
mainMenu()
while status is True:
    print("Let's go!\n")
    for i in range(limit):
        question = getQuestion(choice, excluded)
        print(question.Q)
        user_input = input("> ")
        result = answerCheck(question, user_input)
        if result:
            print("Incorrect! Correct answer is:", result, "\n")
        else:
            score += 1
            print("Correct!\n")
    # Calculate results
    percentage = str(round((score / limit) * 100, 2)) + '%'
    print("Quiz results\n---------------------\n", str(score) + " out of " + str(limit) + " correct\n","Score: " + percentage + "\n")
    # Reset score
    score = 0


    # Ask user if they want to study again
    print("Would you like to study again?")
    user_input = input("> ").lower().strip()
    if user_input == "yes":
        continue
    elif user_input == "quit":
        break
    else:
        status = False

# Exit
print("Goodbye!")
