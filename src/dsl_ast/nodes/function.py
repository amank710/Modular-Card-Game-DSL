from src.dsl_ast.abstract_visitor import AbstractVisitor
from src.dsl_ast.ast_node import AstNode


class BodyNode(AstNode):
    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitBodyNode(self)

        for child in self.children:
            child.accept_player_builder(player_builder)


class IfNode(AstNode):
    def __init__(self, name: str, expression):
        super(IfNode, self).__init__(name=name)

        self.expression = expression

    def get_expression(self):
        return self.expression

    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitIfNode(self)

        for child in self.children:
            child.accept_player_builder(player_builder)

class IfEndContext(AstNode):
    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitIfEndContextNode(self)


class IfElseContext(AstNode):
    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitIfElseContextNode(self)

class LoopNode(AstNode):
    def __init__(self, name: str, expression):
        super(LoopNode, self).__init__(name=name)

        self.expression = expression

    def get_expression(self):
        return self.expression

    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitLoopNode(self)

        for child in self.children:
            child.accept_player_builder(player_builder)

class ContextEndNode(AstNode):
    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitContextEndNode(self)


class FunctionNode(AstNode):
    def __init__(self, name, args=[]):
        super(FunctionNode, self).__init__(name=name)

        self.args = args

    def get_args(self):
        return self.args

    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitFunctionNode(self)

        for child in self.children:
            child.accept_player_builder(player_builder)

class FunctionEndNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitFunctionEndNode(self)

        for child in self.children:
            child.accept_player_builder(player_builder)


class SystemFunctionNode(FunctionNode):
    def __init__(self, name, args=[]):
        super().__init__(name)

        self.args = args

    def get_args(self):
        return self.args

    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitSystemFunctionNode(self)

        for child in self.children:
            child.accept_player_builder(player_builder)

class ActionFunctionNode(FunctionNode):
    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitActionFunctionNode(self)

        for child in self.children:
            child.accept_player_builder(player_builder)

class CommonFunctionsNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitCommonFunctionsNode(self)

        for child in self.children:
            child.accept_player_builder(player_builder)

class UserFunctionsNode(AstNode):
    def __init__(self, name, role):
        super(UserFunctionsNode, self).__init__(name=name)
        self.role = role

    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

    def accept_player_builder(self, player_builder: AbstractVisitor):
        if not player_builder.get_role() == self.role:
            return

        player_builder.visitUserFunctionsNode(self)
        for child in self.children:
            child.accept_player_builder(player_builder)


class ResultNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

    def accept_player_builder(self, player_builder: AbstractVisitor):
        player_builder.visitResultNode(self)
        for child in self.children:
            child.accept_player_builder(player_builder)
