from src.dsl_ast.abstract_visitor import AbstractVisitor
from src.dsl_ast.ast_node import AstNode
from src.game.objects.system_action import PickCard, SystemAction as GameSystemAction


class ActionsNode(AstNode):
    def accept_config_builder(self, config_builder: AbstractVisitor) -> None:
        for child in self.children:
            child.accept_config_builder(config_builder)


class ActionNode(AstNode):
    def get_resolved_action(self):
        raise NotImplementedError

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class SystemActionNode(ActionNode):
    def accept_config_builder(self, config_builder: AbstractVisitor) -> None:
        # All UserActionNode will hopefully resolve to a SystemActionNode
        pass

    def get_resolved_action(self):
        if self.get_name() == "pickCard":
            return PickCard()
        elif self.get_name() == "skipTurn":
            return GameSystemAction.SKIP_TURN
        elif self.get_name() == "waitFor":
            return GameSystemAction.WAIT_FOR
        else:
            raise Exception(
                "Unable to match {} to a System Action!".format(self.get_name()))


class UserActionNode(ActionNode):
    def get_resolved_action(self):
        return GameSystemAction.INVALID

    def accept_config_builder(self, config_builder: AbstractVisitor) -> None:
        config_builder.visitUserActionNode(self)
