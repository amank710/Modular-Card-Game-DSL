from src.factory.cards.card import Card
from src.factory.cards.card_factory import CardFactory
from src.game.objects.system_action import SystemAction
from src.game.objects.variable import Variable

from collections.abc import Set
from typing import Dict, List, Set


class ConfigPrototype:
    def __init__(self):
        self.roles = list()

        self.card_factory = CardFactory()
        self.cards: Dict[str, Card] = self.card_factory.build()

        self.variables_map: dict[str, dict[str, Variable]] = dict()
        self.variables_map[Variable.GLOBAL] = dict()

        self.user_action_map: dict[str, List[SystemAction]] = dict()

    ### Roles ###
    def append_role(self, role: str) -> None:
        self.roles.append(role)

    def get_roles(self) -> List[str]:
        return self.roles

    ### Actions ###
    def set_user_action_map(self, action_map: Dict[str, List[SystemAction]]):
        self.user_action_map = action_map

    def get_user_action_map(self) -> Dict[str, List[SystemAction]]:
        return self.user_action_map

    ### Variables ###
    def add_global_variable(self, name):
        self.variables_map[Variable.GLOBAL][name] = Variable(name=name)

    def add_role_variable(self, role, name):
        if role not in self.variables_map:
            self.variables_map[role] = dict()

        self.variables_map[role][name] = Variable(name=name)

    def get_variables_map(self) -> Dict[str, Dict[str, Variable]]:
        return self.variables_map

    ### Cards ###
    def get_cards(self) -> Dict[str, Card]:
        return self.cards

    def update_card_value(self, key, value) -> None:
        override_cards = self.card_factory.get_all_keys_matching(key)
        for card in override_cards:
            self.cards[card].update_card_value([value])
