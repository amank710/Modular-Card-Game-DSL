from src.factory.function_context.expressions.expression import Expression
from src.factory.function_context.expressions.variable_expression import VariableExpression
from src.factory.function_context.statement import Statement
from src.game.objects.variable import Variable

from typing import Dict

class VariableAssignment(Statement):
    def __init__(self, var_name: str, value: Expression, role: str):
        self.var_name = var_name
        self.value = value
        self.role = role

    def execute(self, variables):
        variables[self.role][self.var_name].set_value(value=self.value.evaluate())

        return None

    def __repr__(self) -> str:
        return "{}.{} = {}\n".format(self.role, self.var_name, self.value)

class IndirectVariableAssignment(VariableAssignment):
    def __init__(self, var_name: str, role: str, variables_map: Dict[str, Dict[str, Variable]]):
        super(IndirectVariableAssignment, self).__init__(var_name=var_name, role=role, value=VariableExpression(variables_map=variables_map, var_name=Variable.INDIRECT_VARIABLE, role=role))

    def __repr__(self) -> str:
        return "{}.{} = {}\n".format(self.role, self.var_name, self.value)
