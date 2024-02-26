from src.factory.function_type import FunctionType
from src.factory.function_context.function_context import FunctionContext
from src.game.objects.game_action import GameAction
from src.game.objects.game_effect import GameEffect, PlayerControlStatus
from src.factory.types.callback_type import CallbackType
from src.factory.prototypes.player_prototype import PlayerPrototype

from typing import Any, Callable, Dict
from src.game.objects.system_action import PickCard, SystemAction
from src.game.objects.variable import Variable


class Player:
    """
    A Player is the representation of a user in a game. It executes the custom logic that a User has written in the
    DSL.
    """

    def __init__(self, prototype: PlayerPrototype):
        self.name: str = prototype.get_name()
        self.local_vars: Dict[str, Dict[str, Variable]] = prototype.get_variables()
        self.callback_map: Dict[str, FunctionContext] = prototype.get_all_callbacks()
        self.action_map: Dict[str, SystemAction] = prototype.get_action_map()

    def setup(self) -> GameEffect:
        return self.callback_map[CallbackType.SETUP].execute()
    
    def get_score(self):
        if 'score' in self.local_vars[self.name]:
            return self.local_vars[self.name]['score'].get_value()

        return None

    def get_local_vars(self) -> Dict[str, Any]:
        return self.local_vars
    """
    For mvp, on_turn has a single line wait_for(user action, user action, ...)
    """
    
    def get_role(self) -> str:
        return self.name
    
    def get_local_vars(self) -> Dict[str, Any]:
        return self.local_vars
    
    def set_user_actions(self, action_map):
        selected_actions = []
        for action, selected in action_map.items():
            if selected:
                selected_actions.append(action.get_user_action())

        if len(selected_actions) == 1:
            # TODO(arun): super jank don't do this
            selected_actions = selected_actions[0]
        self.local_vars[self.name][Variable.INDIRECT_VARIABLE].set_value(selected_actions)

    def update_local_vars(self, role:str, var_name: str, var_value: Any) -> None:
        self.local_vars[role][var_name] = var_value

    def get_system_action(self, action:str) -> None:
        return self.action_map[action][0]

    
    def on_turn(self) -> GameEffect:
        result = self.callback_map[CallbackType.ON_TURN].execute()

        self.end_condition()
        if self.local_vars[self.name]["result"].get_value() == "WIN":
            result.set_player_control_status(PlayerControlStatus.WINNER)
        elif self.local_vars[self.name]["result"].get_value() == "LOST":
            result.set_player_control_status(PlayerControlStatus.LOSER)

        return result

    def on_action(self, ga: GameAction) -> GameEffect:
        # print(ga)
        # action = GameAction(ga).get_user_action()
        action = ga.get_user_action()
        system_action = self.get_system_action(action)
        if isinstance(system_action, PickCard):
            #Execute PickCard to generate random card from 0-51 and store it in PickCard class
            system_action.execute()
            mark_value = system_action.get_mark_value()
            print("Card value: ", mark_value)   
            variable = Variable(name='card')
            variable.set_value(mark_value)
            self.update_local_vars(self.name, 'card', variable)
            
        return self.callback_map[action].execute()

    def end_condition(self) -> GameEffect:
        return self.callback_map[FunctionType.RESULT].execute()


    def get_callback(self):
        return self.callback_map

    def __repr__(self) -> str:
        ret = "---{} OBJECT---\n".format(self.name)

        ret += "callbacks:\n"
        for name, func_context in self.callback_map.items():
            ret += "\t{}\n".format(name)
            ret += "\t{}".format(str(func_context))

        return ret
