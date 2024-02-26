from src.factory.function_context.function_context import FunctionContext
from src.game.objects.game_effect import GameEffect

from typing import Dict


class FunctionRunner(FunctionContext):
    def __init__(self, function_name: str, function_registry: Dict[str, FunctionContext]):
        self.function_name = function_name
        self.function_registry = function_registry

    def execute(self) -> GameEffect:
        return self.function_registry[self.function_name].execute()
