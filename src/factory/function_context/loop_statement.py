from src.factory.function_context.statement import Statement
from src.factory.function_context.expressions.expression import Expression
from src.factory.function_context.function_context import FunctionContext
from src.factory.function_context.skip_statement import SkipStatement
from src.game.objects.variable import Variable
from enum import Enum
from typing import Dict

class LoopStatement(Statement):
    class StatementContext(Enum):
        LOOP = 0

    def __init__(self, conditional: Expression, function_context: FunctionContext):
        self.conditional = conditional
        self.function_context = function_context
        self.statement_context = LoopStatement.StatementContext.LOOP 
        self.num_then_statements = 0
        self.evaluation = 0
        self.loop_counter = 0
    
    def  increment_statements(self):
        if self.statement_context == LoopStatement.StatementContext.LOOP:
            self.num_then_statements += 1

    def execute(self, variables: Dict[str, Variable]):
        self.loop_counter = 0
        if self.conditional.evaluate():
            self.loop_counter += 1
            self.evaluation = 0
            entrypoint = self.function_context.get_entrypoint()
            self.function_context.insert_statement_in_position(statement=LoopEndStatement(self),
                                                               pos=entrypoint+self.num_then_statements+1)
            
        else:
            entrypoint = self.function_context.get_entrypoint()
            self.function_context.insert_statement_in_position(statement=SkipStatement(num_skips=self.num_then_statements),
                                                               pos=entrypoint+1)
    
    def modify_stack_ptr(self, stack_ptr):
        return stack_ptr + self.evaluation

    def __repr__(self) -> str:
        return f"\tLoop: {str(self.conditional)}\n\t\tIterations: {self.loop_counter}\n"
    
class LoopEndStatement(Statement):
    def __init__(self, loop_statement: LoopStatement):
        self.loop_statement = loop_statement
        self.evaluation = 0

    def execute(self, variables: Dict[str, Variable]):
        pass

    def modify_stack_ptr(self, stack_ptr):
        if self.loop_statement.conditional.evaluate():
            return stack_ptr - self.loop_statement.num_then_statements - 1
        return stack_ptr

    def __repr__(self) -> str:
        return "End of loop\n"