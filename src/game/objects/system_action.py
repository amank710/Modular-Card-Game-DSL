from enum import Enum
import random


class SystemAction(str, Enum):
    INVALID = "INVALID"
    PICK_CARD = "PICK CARD"
    WAIT_FOR = "WAIT FOR"
    SKIP_TURN = "SKIP TURN"

class PickCard:
    def __init__(self) -> None:
        self.card = 0
        self.value = SystemAction.PICK_CARD
    
    def get_value(self) -> str:
        return self.card
    
    def get_mark_value(self) -> int:
        return self.card % 13 + 1
    
    def execute(self):
        self.card = random.randint(0, 51)
        return self.card
    
