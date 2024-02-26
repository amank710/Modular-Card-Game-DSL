from typing import List


class Card:
    def __init__(self, name: str, values: List[int]) -> None:
        self.name = name
        self.values = values

    def get_card(self):
        return (self.name, self.values)

    def get_name(self) -> str:
        return self.name

    def get_values(self):
        return self.values

    def update_card_value(self, values):
        self.values = values

    # To use in frontend
    def get_game_asset(self):
        raise NotImplementedError
