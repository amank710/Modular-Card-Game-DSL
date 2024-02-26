from enum import Enum
from typing import Dict
from src.factory.function_context.expressions.expression import Expression
from src.factory.function_context.function_context import FunctionContext
from src.factory.function_context.skip_statement import SkipStatement
from src.factory.function_context.statement import Statement
from src.game.objects.variable import Variable


class IfStatement(Statement):
    class StatementContext(Enum):
        IF = 0
        ELSE = 1

    # Assume func_statement a function statement that can be executed
    def __init__(self, conditional: Expression, function_context: FunctionContext):
        self.conditional = conditional

        self.num_then_statements = 0
        self.num_else_statements = 0

        self.function_context = function_context

        self.statement_context = IfStatement.StatementContext.IF

        self.evaluation = 0

    def switch_context(self):
        self.statement_context = IfStatement.StatementContext.ELSE

    def increment_statements(self):
        if self.statement_context == IfStatement.StatementContext.IF:
            self.num_then_statements += 1
        elif self.statement_context == IfStatement.StatementContext.ELSE :
            self.num_else_statements += 1

    def execute(self, variables: Dict[str, Variable]):
        if self.conditional.evaluate():
            self.evaluation = 0
            entrypoint = self.function_context.get_entrypoint()
            self.function_context.insert_statement_in_position(statement=SkipStatement(num_skips=self.num_else_statements),
                                                               pos=entrypoint+self.num_then_statements+1)
        else:
            self.evaluation = self.num_then_statements

    def modify_stack_ptr(self, stack_ptr):
        return stack_ptr + self.evaluation

    def __repr__(self) -> str:
        ret = "\tif: {}\n".format(str(self.conditional))
        ret += "\t\ttrue: at +{} index, skip {} statements\n".format(self.num_then_statements, self.num_else_statements)
        ret += "\t\tfalse: skip next {} statements\n".format(self.num_else_statements)

        return ret
