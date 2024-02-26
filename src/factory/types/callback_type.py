from enum import Enum


class CallbackType(str, Enum):
    """
    The system callbacks that a user can override
    """
    SETUP = "setup"
    ON_TURN = "on_turn"
    RESULT = "result"
