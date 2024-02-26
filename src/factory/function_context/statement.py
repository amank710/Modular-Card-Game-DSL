from src.game.objects.game_effect import GameEffect
from src.game.objects.variable import Variable

from typing import Dict, Union


class Statement:
    def execute(self, variables: Dict[str, Dict[str, Variable]]) -> Union[GameEffect, None]:
        raise NotImplementedError

    def modify_stack_ptr(self, stack_ptr: int) -> int:
        return stack_ptr
