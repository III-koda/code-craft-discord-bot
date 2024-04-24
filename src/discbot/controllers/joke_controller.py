from random import randint

from static_data.jokes import JOKES


def joke_generator():
    idx = randint(0, len(JOKES) - 1)
    return "```" + JOKES[idx] + "```"
