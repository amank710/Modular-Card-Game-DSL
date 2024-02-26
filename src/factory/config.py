from src.factory.cards.card import Card
from src.game.objects.system_action import SystemAction
from src.game.objects.variable import Variable

from typing import Dict, List

from .prototypes.config_prototype import ConfigPrototype


class Config:
    """
    Config is the representation of the config code block written by the user.
    Requires: Clean AST of Config
    Effects: Parses AST to intialize functions for cards, roles, actions, and variables
    """

    def __init__(self, config_prototype: ConfigPrototype):
        self.cards: Dict[str, Card] = config_prototype.get_cards()

        self.roles: List[str] = config_prototype.get_roles()
        self.variables_map: Dict[str, Dict[str, Variable]] = config_prototype.get_variables_map()
        self.actions: dict[str, List[SystemAction]
                           ] = config_prototype.get_user_action_map()

    def get_cards(self):
        return self.cards

    def get_roles(self) -> List[str]:
        return self.roles

    def get_corresponding_system_function(self, user_action):
        return self.actions[user_action]

    def get_user_actions(self) -> List[SystemAction]:
        return self.actions.keys()

    def get_action_mapping(self):
        return self.actions

    def get_variables(self) -> Dict[str, Dict[str, Variable]]:
        return self.variables_map

    def __repr__(self) -> str:
        ret = "---CONFIG OBJECT---\n"

        ret += "ROLES\n"
        for role in self.roles:
            ret += "\t{}\n".format(role)

        for role in self.variables_map.keys():
            ret += "{}'s VARIABLES\n".format(role)
            for variable_name in self.variables_map[role].keys():
                ret += "\t{}\n".format(variable_name)

        ret += "ACTIONS\n"
        for action in self.actions.keys():
            ret += "\t{}:\n".format(action)
            for system_action in self.actions[action]:
                ret += "\t\t{}\n".format(str(system_action))

        ret += "CARDS\n"
        for card in self.cards.values():
            ret += "\t{}: {}\n".format(card.get_name(), str(card.get_values()))

        return ret
