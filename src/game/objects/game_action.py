from typing import List


class GameAction:
    def __init__(self, user_action, sys_action=None) -> None:
        self.user_action = user_action
        self.sys_action = sys_action
        self.current_card = 0
    
    def set_current_card(self, card):
        self.current_card = card
    
    def get_current_card(self):
        return self.current_card
    
    def get_system_action(self):
        return self.sys_action
    
    def set_system_action(self, sys_action):
        self.sys_action = sys_action

    def get_user_action(self) -> str:
        return self.user_action

    def get_sys_action(self):
        return self.sys_action

    def __repr__(self):
        ret = "GameAction, card: {}, user_action: {}, system_action: {}".format(self.current_card, self.user_action, self.sys_action)
        return ret
