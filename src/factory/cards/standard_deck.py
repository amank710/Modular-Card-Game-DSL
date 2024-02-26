from src.factory.cards.card import Card

from enum import Enum
from typing import Dict


class StandardCard(Card):
    pass


class StandardDeck():
    class Suite(Enum):
        heart = 0
        spade = 1
        clubs = 2
        diamond = 3

    class Value(Enum):
        ace = 1
        two = 2
        three = 3
        four = 4
        five = 5
        six = 6
        seven = 7
        eight = 8
        nine = 9
        ten = 10
        jack = 11
        queen = 12
        king = 13

    def card_rep(self, key: str, suite: str):
        return "{} {}".format(key, suite)

    def build(self) -> Dict[str, Card]:
        # TODO(arun): handle jokers in the standrd deck
        all_cards_vals = [StandardCard(name=self.card_rep(val.name, suite.name), values=[val.value])
                          for val in StandardDeck.Value for suite in StandardDeck.Suite]

        return {card.get_name(): card for card in all_cards_vals}

    def get_all_keys_matching(self, key):
        return [self.card_rep(key, suite.name) for suite in StandardDeck.Suite]
