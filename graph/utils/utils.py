from random import randrange, choice

def autoinc():
    n = 0
    while True:
        n += 1
        yield n

vowels = "eyuioa"
consonants = "qwrtpsdfghjklzxcvbnm"
max_consonants_in_row = 2

def generate_city_name() -> str:
    """Generate a random name of an alien city.

    A-Z letters are picked randomly; chances of a vowel vary
    from 10% to 100% (after 2 consonants in a row).
    """
    name = ""
    length = randrange(4, 11)
    vowel_chance = 10 # %
    while len(name) < length:
        if randrange(100) < vowel_chance:
            name += choice(vowels)
            vowel_chance = 10
        else:
            name += choice(consonants)
            vowel_chance += 100 / max_consonants_in_row
    return name.title()
