from . import utils

if __name__ == "__main__":
    ai = utils.Autoinc()
    assert ai.next() == 1
    assert ai.next() == 2

    ai.use(100)
    assert ai.next() == 101

    ai.use(5)
    assert ai.next() == 102
    print("✅ Autoinc() assertion ok.")
