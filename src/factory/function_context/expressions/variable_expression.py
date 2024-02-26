from src.factory.function_context.expressions.expression import Expression
from src.game.objects.variable import Variable

from typing import Dict

class VariableExpression(Expression):
    def __init__(self, variables_map: Dict[str, Dict[str, Variable]], var_name, role):
        self.variables_map = variables_map
        self.var_name = var_name
        self.role = role

    def evaluate(self):
        print(self.variables_map[self.role])
        return self.variables_map[self.role][self.var_name].get_value()

    def __repr__(self) -> str:
        return "VAR: {}.{}".format(self.role, self.var_name)
