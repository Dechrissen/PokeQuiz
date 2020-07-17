# PokeQuiz

PokeQuiz is a command line studying tool that allows you to test your knowledge by answering randomly-generated Pokemon questions. Currently, data from generations 1 – 7 is included, but I do have plans to add generation 8 and *possibly* side-games such as Colosseum and XD Gale of Darkness in later releases.  
  
PokeQuiz ships with a lightweight SQLite database containing information on:
- Pokemon
- Regions (Kanto, Johto, etc.)
- Towns
- Gym Leaders
- Enemy Teams (Rocket, Magma, etc.)
- Games (Red & Blue, Silver & Gold, etc.)



## Installation
To install via pip, go to your terminal and run:
```cmd
> pip install pokequiz
```

To install from source, download the latest release [here](https://github.com/Dechrissen/PokeQuiz/releases). Make sure to `cd` into the directory of the source files and and run:
```cmd
> python setup.py install
```

## Usage
Installing PokeQuiz will add an entry point to your PATH named `pokequiz`.  
  
To run PokeQuiz from your terminal, simply run:
```cmd
> pokequiz
```
or
```cmd
> python -m pokequiz
```

### How to use the PokeQuiz Main Menu
```
------------------------------
     Welcome to PokeQuiz!
------------------------------
       -----------------
           Main Menu
       -----------------

1 - Start Quiz
2 - Study Categories
3 - Marathon Mode
4 - Settings
5 - Set Seed
6 - Help
7 - Quit

>
```

`Start Quiz`  
This will give you a 20-question quiz.

`Study Categories`  
This will give you a 20-question quiz restricted to ONE category.

`Marathon Mode`  
This will give you an endless quiz. Type 'quit' at any time to exit.

`Settings`  
Here you can edit global settings (generation filtering and question limit) before studying.  

`Set Seed`  
Enter a seed to challenge others to the same quiz.


### Sample Questions
```
Fuchsia City is a town in what region?
```
```
Who is the Champion in Platinum version?
```
```
What evolves into Altaria?
```
```
Team Aqua is the enemy team in what region?
```
```
Who is the professor in Kalos?
```

### Seeds
PokeQuiz supports set quiz seeds to generate identical quizzes in order to challenge others and compare scores. All seeds will invoke a 20-question quiz with no restriction on Pokemon generation or question type.  
  
Currently supported seeds: 1-100
