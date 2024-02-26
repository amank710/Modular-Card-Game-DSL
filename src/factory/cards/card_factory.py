from src.factory.cards.standard_deck import StandardDeck
from src.factory.cards.card import Card

from typing import Dict


class CardFactory:
    def __init__(self):
        self.deck = StandardDeck()

    def build(self) -> Dict[str, Card]:
        return self.deck.build()

    def get_all_keys_matching(self, key):
        return self.deck.get_all_keys_matching(key)

    # for the frontend
    def game_asset(self):
        raise NotImplementedError
