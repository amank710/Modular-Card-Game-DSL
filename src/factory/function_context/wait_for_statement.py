from typing import Dict, List, Union
from src.factory.config import Config
from src.factory.function_context.statement import Statement
from src.game.objects.game_action import GameAction
from src.game.objects.game_effect import GameEffect, PlayerControlStatus
from src.game.objects.variable import Variable


class WaitForStatement(Statement):
    def __init__(self, args, config: Config):
        self.actions = args
        self.config = config

    def execute(self, variables: Dict[str, Dict[str, Variable]]) -> Union[GameEffect, None]:
        game_effect = GameEffect(PlayerControlStatus.IN_PROGRESS) 

        for action in self.actions:
            eval_action = action.evaluate()
            game_effect.append_game_action(
                    GameAction(user_action=eval_action,
                                            sys_action=self.config.get_corresponding_system_function(user_action=eval_action)))

        return game_effect

    def __repr__(self) -> str:
        return "waitFor({})\n".format(str(self.actions))
