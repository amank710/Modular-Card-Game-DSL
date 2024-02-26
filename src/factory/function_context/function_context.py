from src.game.objects.game_effect import PlayerControlStatus
from src.factory.function_context.statement import Statement
from src.factory.function_context.variable_assignment import VariableAssignment
from src.game.objects.game_effect import GameEffect
from src.game.objects.variable import Variable

from typing import Dict, List


class FunctionContext:
    # a list of executable statements (e.g variable assignment, conditional, loop etc.)

    # Assume func_statement a function statement that can be executed
    def __init__(self, variables: Dict[str, Variable], name: str="noop"):
        self.name = name
        self.statements: List[Statement] = []
        self.committed_statements: List[Statement]
        self.variables = variables

        self.entrypoint = 0  # entrypoint into the statements list


    def set_context_end(self):
        self.committed_statements = self.statements.copy()

    def get_name(self):
        return self.name

    def add_statement(self, statement: Statement):
        self.statements.append(statement)

    def get_entrypoint(self):
        return self.entrypoint

    def insert_statement_in_position(self, statement: Statement, pos: int):
        self.statements.insert(pos, statement)
        
    def get_statements(self): 
        return self.statements

    def execute(self) -> GameEffect:
        if self.entrypoint == 0:
            self.statements = self.committed_statements.copy()

        while self.entrypoint < len(self.statements):
            ret = None
            ret = self.statements[self.entrypoint].execute(self.variables)
            self.entrypoint = self.statements[self.entrypoint].modify_stack_ptr(self.entrypoint)
            if self.entrypoint > len(self.statements):
                self.entrypoint = 0
                if ret is not None:
                    return ret
                return GameEffect(status=PlayerControlStatus.TURN_DONE)
            self.entrypoint = (self.entrypoint + 1) % (len(self.statements)+1)
            if ret is not None:
                return ret

        self.entrypoint = 0
        return GameEffect()

    def __repr__(self) -> str:
        ret = ""
        for i in range(len(self.statements)):
            ret += "{}: ".format(i) + str(self.statements[i])

        if len(self.statements) == 0:
            ret += "\n"

        return ret
