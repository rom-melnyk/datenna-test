from random import randrange, choice

class Autoinc:
    """Simple autoincrement implementation."""
    def __init__(self):
        self.index = 0

    def next(self) -> int:
        """Return next index."""
        self.index += 1
        return self.index

    def use(self, used_index: int):
        """Mark given index as "used" so futher `next()` don't overlap with it."""
        if used_index > self.index:
            self.index = used_index

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
