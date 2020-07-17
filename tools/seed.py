from Classes import *
from Question import getQuestion
import random
import json

# This script is used to generate "seeds" and corresponding random Q/A pairs saved to a json file


# generate 1-100 (no restrictions)
choice = None
excluded = []
last_twenty = []
num_of_seeds = 100
num_of_q = 20
print("Creating seeds 1-100...")
with open('seeds.json', 'w') as f:
    seeds_dict = {}
    for i in range(num_of_seeds):
        quiz_dict = {}
        for n in range(num_of_q):
            question = getQuestion(choice, excluded, last_twenty)
            quiz_dict[n+1] = [question.Q, question.A]
        seeds_dict[i+1] = quiz_dict
    f.write(json.dumps(seeds_dict))
print("Done.")
