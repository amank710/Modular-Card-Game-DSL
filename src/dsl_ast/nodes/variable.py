from src.dsl_ast.abstract_visitor import AbstractVisitor
from src.dsl_ast.ast_node import AstNode
from src.dsl_ast.expression import ExpressionNode
from src.dsl_ast.nodes.function import FunctionNode
from src.game.objects.variable import Variable


### VARIABLE DECLARATION ###
class VariableDeclarationsNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        for child in self.children:
            child.accept_config_builder(config_builder)


class VariableDeclarationNode(AstNode):
    def __init__(self, name):
        super(VariableDeclarationNode, self).__init__(name=name)
        self.value = None

    def set_value(self, val):
        self.value = val

    def get_role(self):
        raise NotImplementedError


class VariableDeclarationGlobalNode(VariableDeclarationNode):
    def accept_config_builder(self, config_builder: AbstractVisitor) -> None:
        config_builder.visitVariableDeclarationGlobalNode(self)

    def get_role(self):
        return Variable.GLOBAL


class VariableDeclarationRoleNode(VariableDeclarationNode):
    def __init__(self, name, scope):
        super(VariableDeclarationRoleNode, self).__init__(name=name)
        self.role = scope

    def get_string_rep(self):
        return repr(self.name) + " (" + str(self.role) + ": " + str(type(self).__name__) + ")"

    def accept_config_builder(self, config_builder: AbstractVisitor) -> None:
        config_builder.visitVariableDeclarationRoleNode(self)

    def get_role(self) -> str:
        return self.role

### VARIABLE ASSIGNMENT ###
class VariableAssignmentNode(AstNode):
    def __init__(self, name: str, value, role: str):
        super(VariableAssignmentNode, self).__init__(name=name)

        self.role = role
        self.value = value

    def get_value(self):
        return self.value

    def get_role(self):
        return self.role

    def get_string_rep(self):
        return repr(self.name) + " (" + str(self.role) + ": " + str(type(self).__name__) + ")"


class DirectVariableAssignmentNode(VariableAssignmentNode):
    def __init__(self, access_context: VariableDeclarationNode, value: ExpressionNode):
        var_name = access_context.get_name()
        role = access_context.get_role()
        value = value

        super(DirectVariableAssignmentNode, self).__init__(name=var_name, value=value, role=role)

    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitDirectVariableAssignmentNode(self)

class DelayedVariableAssignmentNode(VariableAssignmentNode):
    def __init__(self, access_context: VariableDeclarationNode, delay_function: FunctionNode):
        var_name = access_context.get_name()
        role = access_context.get_role()
        value = delay_function

        super(DelayedVariableAssignmentNode, self).__init__(name=var_name, value=value, role=role)

    def accept_player_builder(self, player_builder: AbstractVisitor):
        self.value.accept_player_builder(player_builder)

        player_builder.visitIndirectVariableAssignmentNode(self)
