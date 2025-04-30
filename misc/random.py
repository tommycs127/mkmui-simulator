import random


def flip_coin() -> int:
    return random.randint(0, 1)
    
def random_choice(list_: list) -> object:
    return random.choice(list_)
