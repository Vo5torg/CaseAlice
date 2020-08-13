from enum import Enum


class State(Enum):
    CREATE_USER = -1
    MENU = 0
    CHOOSE_OPEN_CASE = 1
    OPEN = 2
    STATISTICS = 3
    TOP = 4


State.ALL = tuple(State)
