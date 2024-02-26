from src.game.objects.game_action import GameAction

from enum import Enum
from typing import Dict


class PlayerControlStatus(Enum):
    """
    The control status of a Player in the current turn.
    """
    UNKNOWN = -2
    QUIT = -1
    TURN_DONE = 0
    IN_PROGRESS = 1
    WINNER = 10
    LOSER = -10


class GameEffect:
    """
    A GameEffect summarizes how the Player has affected the World (game) using the system Actions during their turn.

    It comprises of:
    1. Whether the Player is still in charge of the turn (don't transition to a different Player)
    2. The series of Actions that the Game must apply that a user decided
    """

    def __init__(self, status: PlayerControlStatus = PlayerControlStatus.TURN_DONE) -> None:
        self.status: PlayerControlStatus = status
        self.game_actions: Dict[GameAction, bool] = {}
        self.current_card = 10
        self.score = None

    def append_game_action(self, game_action: GameAction) -> None:
        game_action.set_current_card(self.get_current_card())
        self.game_actions[game_action] = False

    def get_actions(self) -> Dict[GameAction, bool]:
        """
        Returns a list of possible GameActions for UI to display.
        """
        return self.game_actions

    def set_current_card(self, card: int):
        self.current_card = card

    def get_current_card(self) -> int:
        return self.current_card

    def set_score(self, score: int):
        self.score = score

    def get_score(self):
        return self.score
    
    def set_game_action(self, game_action: GameAction):
        """
        UI should pass every action a user select to this function
        """
        self.game_actions[game_action] = True 
    
    def set_player_control_status(self, status:PlayerControlStatus):
        self.status = status

    def get_player_control_status(self) -> PlayerControlStatus:
        return self.status

    def __repr__(self):
        ret = "---Game Effect---\n"
        ret += "player control status: {}\n".format(str(self.status))
        ret += "current_card: {}\n".format(str(self.current_card))
        for action, enabled in self.game_actions.items():
            if enabled:
                ret += "ENABLED {}\n".format(str(action))
            else:
                ret += "DISABLED {}\n".format(str(action))

        return ret
        
"""
Game Module -> Game Actions -> Game Effect object
Push game effect object to the queue 
Dequeue and show action options via PyGame
Based on user choice -> Push another object to queue
Dequeue in game module and do the required action
"""
