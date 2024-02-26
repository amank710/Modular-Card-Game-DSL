from src.dsl_ast.nodes.action import ActionNode, UserActionNode
from src.dsl_ast.nodes.variable import VariableDeclarationGlobalNode, VariableDeclarationRoleNode
from src.dsl_ast.ast_node import ConfigurationNode, ProgramNode, CardNode, RoleNameNode
from src.factory.prototypes.config_prototype import ConfigPrototype
from src.dsl_ast.abstract_visitor import AbstractVisitor
from src.game.objects.system_action import SystemAction

from typing import Dict, List


class ConfigBuilder(AbstractVisitor):
    def __init__(self):
        self.config_obj = ConfigPrototype()

        self.mapped_actions: Dict[UserActionNode, List[ActionNode]] = dict()

    def build(self, root_node: ProgramNode) -> ConfigPrototype:
        root_node.accept_config_builder(self)

        action_map: dict[str, List[SystemAction]] = dict()
        for user_action_name in self.mapped_actions:
            action_map[user_action_name.get_name()] = self.resolve_actions(
                user_action_name)
        self.config_obj.set_user_action_map(action_map)

        return self.config_obj

    def resolve_actions(self, action: ActionNode) -> List[SystemAction]:
        resolved_actions = list()
        for related_action in action.children:
            resolution = [related_action.get_resolved_action()]
            if resolution[0] == SystemAction.INVALID:
                resolution = self.resolve_actions(action=related_action)

            resolved_actions += resolution

        return resolved_actions

    def visitCardNode(self, node: CardNode) -> None:
        key, value = node.get_card_mapping()
        self.config_obj.update_card_value(key=key, value=value)

    def visitRoleNameNode(self, node: RoleNameNode) -> None:
        self.config_obj.append_role(node.get_name())

    def visitVariableDeclarationGlobalNode(self, node: VariableDeclarationGlobalNode) -> None:
        self.config_obj.add_global_variable((node.get_name()))

    def visitVariableDeclarationRoleNode(self, node: VariableDeclarationRoleNode) -> None:
        self.config_obj.add_role_variable(
            role=node.get_role(), name=node.get_name())

    def visitUserActionNode(self, node) -> None:
        if node not in self.mapped_actions:
            self.mapped_actions[node] = list()

        for child in node.children:
            self.mapped_actions[node].append(child)
