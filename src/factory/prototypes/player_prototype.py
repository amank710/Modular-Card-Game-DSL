from src.factory.function_context.function_context import FunctionContext
from src.factory.types.callback_type import CallbackType
from src.game.objects.variable import Variable

from typing import Dict, List


class PlayerPrototype:
    """
    A PlayerPrototype is used when parsing the AST to set up the user-defined functionality (local variables and
    custom user functions).
    """

    def __init__(self, name: str, actions: List[str], variables: Dict[str, Dict[str, Variable]]) -> None:
        self.name = name
        self.callback_map: Dict[str, FunctionContext] = dict()
        self.variables = variables

        self.callback_map[CallbackType.SETUP] = FunctionContext(variables=self.variables)
        self.callback_map[CallbackType.ON_TURN] = FunctionContext(variables=self.variables)

        self.variables[self.name][Variable.INDIRECT_VARIABLE] = Variable(name=Variable.INDIRECT_VARIABLE)

        self.action_map = dict()
        for action in actions:
            self.callback_map[action] = FunctionContext(variables=self.variables)


    def register_callback(self, callback_type: str, callback: FunctionContext) -> None:
        self.callback_map[callback_type] = callback
    
    def register_action_map(self, action_map) -> None:
        self.action_map = action_map
        
    def get_action_map(self):
        return self.action_map

    def get_variables(self) -> Dict[str, Dict[str, Variable]]:
        return self.variables

    def get_all_callbacks(self) -> Dict[str, FunctionContext]:
        return self.callback_map

    def get_name(self) -> str:
        return self.name

    def get_end_condition(self):
        return NotImplementedError

    def set_end_condition(self):
        return NotImplementedError
