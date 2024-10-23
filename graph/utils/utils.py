from random import randint, choice

def autoinc():
    n = 0
    while True:
        n += 1
        yield n

def generate_city_name() -> str:
    """Generate a random name of an alien city.
    A-Z letters are picked randomly; chances of a vowel vary
    from 10% to 100% (after 3 consonants in a row).
    """
    vowels = "eyuioa"
    consonants = "qwrtpsdfghjklzxcvbnm"
    name = ""
    length = randint(4, 10)
    vowel_chance = 10
    while len(name) < length:
        if randint(1, 100) <= vowel_chance:
            name += choice(vowels)
            vowel_chance = 10
        else:
            name += choice(consonants)
            vowel_chance += 30
    return name[0].upper() + name[1:]
