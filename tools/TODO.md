# TODO

- user profiles and high scores?
- passwords / easter eggs
- special seeds for gen 1 only, 50 q, etc.
- congratulate with question streaks and delayed one line printing
- add args to pokequiz command line command from stackoverflow link about entry points
- Seeds are broken. Since they don't have type of PokemonQuestion and type 4, they don't go through special case check in
answerCheck. So Pokemon type questions are incorrectly normal list questions, i.e. Type1 or Type2 instead of Type1 & Type2. Fix
this by possibly adding a check in SeedQuestion to check if the list in the answer includes Pokemon Types from a preset list. If
yes, then give it a type of 4 just like PokemonQuestion. Then add a check in the special case check to let it be PokemonQuestion
OR SeedQuestion. Then regenerate seeds.
