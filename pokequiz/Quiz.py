import random
import sqlite3
from Classes import *
from Question import getQuestion, getSeed, answerCheck
import time


# Settings
limit = 20 # Question limit
excluded = [] # Excluded gens
status = True # Continue status
choice = None # Question type (None by default, because all are included)
last_twenty = [] # Store of last 20 questions to avoid duplicates
seed = None

def mainMenu():
    global limit
    global seed
    print("       -----------------\n           Main Menu\n       -----------------\n")
    print("1 - Start Quiz")
    print("2 - Study Categories")
    print("3 - Marathon Mode")
    print("4 - Settings")
    print("5 - Set Seed")
    print("6 - Help")
    print("7 - Quit\n")
    user_input = input("> ").strip()
    if user_input == '1':
        return
    elif user_input == '2':
        individualCategories()
    elif user_input == '3':
        limit = 1000
    elif user_input == '4':
        settings()
    elif user_input == '5':
        print("Enter a seed:")
        given_seed = input("> ").strip()
        if given_seed == '':
            print("Invalid input.\nReturning to main menu...\n")
            mainMenu()
        else:
            seed = given_seed
            limit = 20
    elif user_input == '6':
        print("How to use PokeQuiz\n-------------------")
        print("'Start Quiz' - This will give you a 20-question quiz.\n")
        print("'Study Categories' - This will give you a 20-question quiz restricted to ONE category.\n")
        print("'Marathon Mode' - This will give you an endless quiz. Type 'quit' at any time to exit.\n")
        print("'Set Seed' - Enter a seed to challenge others to the same quiz.\n")
        print("'Settings' - Here you can edit global settings (generation filtering and question limit) before studying.\n")
        waiting = input("Press any key to return... ")
        print("")
        mainMenu()
    else:
        print("Goodbye!")
        quit()

def individualCategories():
    global choice
    print("       ------------------\n           Categories\n       ------------------\n")
    print("1 - Study Pokemon")
    print("2 - Study Games")
    print("3 - Study Regions")
    print("4 - Study Towns")
    print("5 - Study Gym Leaders")
    print("6 - Study Teams")
    print("7 - Study All")
    print("8 - Back to Main Menu")
    print("9 - Quit\n")
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
        choice = None
    elif user_input == '8':
        mainMenu()
    else:
        print("Goodbye!")
        quit()

def settings():
    global limit
    global excluded
    print("       ----------------\n           Settings\n       ----------------\n")
    print("1 - Filter Generations")
    print("2 - Set Question Limit")
    print("3 - Current Settings")
    print("4 - Back to Main Menu")
    print("5 - Quit\n")
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
        print("Returning to main menu...\n")
        mainMenu()
    elif user_input == '2':
        print("Enter desired number of questions per quiz:")
        num = input("> ").strip()
        try:
            limit = int(num)
            print("Question limit set to", num, "\nReturning to main menu...\n")
            mainMenu()
        except ValueError:
            print("Invalid input.\nReturning to main menu...\n")
            mainMenu()
    elif user_input == '3':
        print("Current Settings\n----------------")
        print("Question limit:", limit)
        print("Excluded generations:", ", ".join(excluded) if excluded else "None", "\n")
        waiting = input("Press any key to return... ")
        print("")
        settings()
    elif user_input == '4':
        mainMenu()
    else:
        print("Goodbye!")
        quit()


# Main program
def quiz(status):
    global limit
    print("------------------------------\n     Welcome to PokeQuiz!\n------------------------------")
    mainMenu()
    if seed:
        seed_quiz = getSeed(seed)
    while status is True:
        score = 0
        print("Let's go!\n")
        for i in range(limit):
            if seed:
                question = seedQuestion(*seed_quiz[str(i + 1)])
            else:
                question = getQuestion(choice, excluded, last_twenty)
            print('#' + (str(i + 1)) + ': ' + question.Q)
            user_input = input("> ")
            result = answerCheck(question, user_input)
            if result:
                print("Incorrect! Correct answer is:", result, "\n")
            else:
                score += 1
                print("Correct!\n")
        # Calculate results
        percentage = str(round((score / limit) * 100, 2)) + '%'
        print("----------------------\n     Quiz Results\n----------------------\n", str(score) + " out of " + str(limit) + " correct\n","Score: " + percentage)
        if seed:
            print(" Seed:", seed, "\n")
        else:
            print("\n")
        # Ask user if they want to study again
        print("Would you like to study again?")
        user_input = input("> ").lower().strip()
        if user_input == "yes" or user_input == 'y':
            continue
        else:
            status = False
    # Exit
    print("Goodbye!")
    quit()

# Start
quiz(status)
