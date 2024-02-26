from src.dsl_ast.abstract_visitor import AbstractVisitor


class AstNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children is not None else []

    def get_name(self):
        return self.name

    def add_child(self, child):
        self.children.append(child)

    def accept_config_builder(self, config_builder: AbstractVisitor) -> None:
        raise NotImplementedError

    def accept_player_builder(self, player_builder: AbstractVisitor) -> None:
        raise NotImplementedError

    def get_string_rep(self):
        return repr(self.name) + " (" + str(type(self).__name__) + ")"

    def __repr__(self, level=0, prefix=""):
        print(type(self))
        indent = "  "
        vertical_line = "| "
        if level > 0:
            prefix = prefix + vertical_line
        ret = prefix + self.get_string_rep() + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1, prefix + indent)
        return ret


class ProgramNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        for child in self.children:
            child.accept_config_builder(config_builder)

    def accept_player_builder(self, player_builder: AbstractVisitor):
        for child in self.children:
            child.accept_player_builder(player_builder)


class ConfigurationNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        for child in self.children:
            child.accept_config_builder(config_builder)

    def accept_player_builder(self, player_builder: AbstractVisitor):
        pass


class CardNode(AstNode):
    def __init__(self, key: str):
        super(CardNode, self).__init__(name=key)
        self.values = []

    def get_card_mapping(self):
        return self.name, self.values

    def add_value(self, val):
        self.values.append(val)

    def accept_config_builder(self, config_builder: AbstractVisitor):
        config_builder.visitCardNode(self)

    def get_string_rep(self):
        return super().get_string_rep() + ": " + str(self.values)


class RoleNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        for child in self.children:
            child.accept_config_builder(config_builder)


class RoleNameNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        config_builder.visitRoleNameNode(self)


class CardsNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        for child in self.children:
            child.accept_config_builder(config_builder)


class UserNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass


class VariableAssigneeNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass


class CardValueOverrideNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        for child in self.children:
            child.accept_config_builder(config_builder)


class GameNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

    def accept_player_builder(self, player_builder: AbstractVisitor):
        for child in self.children:
            child.accept_player_builder(player_builder)


class FunctionBodyNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass

class OperatorNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor):
        pass
