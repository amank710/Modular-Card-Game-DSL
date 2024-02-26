from src.factory.function_context.statement import Statement
from src.game.objects.game_effect import GameEffect
from src.game.objects.variable import Variable

from typing import Dict, Union

class SkipStatement(Statement):
    def __init__(self, num_skips: int):
        self.num_skips = num_skips

    def execute(self, variables: Dict[str, Dict[str, Variable]]) -> Union[GameEffect, None]:
        pass

    def modify_stack_ptr(self, stack_ptr: int) -> int:
        return stack_ptr + self.num_skips

    def __repr__(self) -> str:
        return "skip {} statements".format(self.num_skips)
