from . import utils

if __name__ == "__main__":
    ai = utils.autoinc()
    while next(ai) < 10:
        print(utils.generate_city_name())
