import logging
import copy
from src.game.objects.game_action import GameAction
from src.factory.player import Player
from src.factory.prototypes.game_prototype import GamePrototype
from src.game.objects.game_effect import GameEffect, PlayerControlStatus
from queue import Queue

logging.getLogger().setLevel(logging.CRITICAL)

class Game:
    """
    The Game class handles the gameplay logic. It is responsible for:
    - Setting up the Game
    - Executing the turn mechanisms of the Players
    - Checking if the game end state has been reached and declaring the winner
    """
    def __init__(self, game_proto: GamePrototype, prod_queue=Queue(maxsize=10), cons_queue=Queue(maxsize=10)) -> None:
        self.roles = game_proto.get_all_players()

        self.prod_queue = prod_queue
        self.cons_queue = cons_queue

        self.running = True

    def finish_turn(self, status):
        if status == PlayerControlStatus.UNKNOWN or status == PlayerControlStatus.IN_PROGRESS:
            return False

        return True

    def end_game(self, status):
        if status == PlayerControlStatus.QUIT or status == PlayerControlStatus.WINNER or status == PlayerControlStatus.LOSER:
            return True

        return False

    def turn_manager(self):
        while self.running:
            for player in self.roles:
                status = PlayerControlStatus.UNKNOWN
                while not self.finish_turn(status):
                    logging.info("{} executing a turn".format(player.get_role()))
                    output = player.on_turn()
                    output.set_score(score=player.get_score())
                    self.produce_game_effect(output)
                    effect = self.consume_game_effect()
                    player.set_user_actions(effect.get_actions())
                    status = effect.get_player_control_status()
                    logging.info("Game: consumed response: {}".format(str(effect)))
                    user_acts = effect.get_actions().keys()
                    act_map = effect.get_actions()
                    for act in user_acts:
                        if act_map[act]:
                            player.on_action(act)

                    logging.debug("[Game] At end of turn, state of user variables: {}" + str(player.get_local_vars()))

                if self.end_game(status):
                    self.running = False
                    logging.info("[Game] Game over!")
                    break

    
        

    def turn1(self) -> bool:
        current_effect = self.dequeue_next()
        # Pass the effect to the UI here; UI should then push the effect with newly changed bools to consumer queue
        # We're mocking what the ui is doing here for now, setting first action to have been selected by user
        current_effect.set_game_action(list(current_effect.get_actions().keys())[0])
        self.cons_queue.put(current_effect)
        
        # Get the actions chosen by the user
        act_map = self.consume_game_effect().get_actions()
        user_acts = act_map.keys()
        self.role1.set_user_actions(act_map)
        for act in user_acts:
            if act_map[act]: 
                self.role1.on_action(act.get_user_action())
            
            handle_act: bool = self.turn(self.role1)
            if not handle_act:
                return handle_act
    
        # Once all actions are completed, communicate turn done to UI
        self.produce_game_effect(GameEffect(PlayerControlStatus.TURN_DONE))
        return True

    def turn2(self) -> bool:
        current_effect = self.dequeue_next()
        # Pass the effect to the UI here; UI should then push the effect with newly changed bools to consumer queue
        # We're mocking what the ui is doing here for now, setting first action to have been selected by user
        current_effect.set_game_action(list(current_effect.get_actions().keys())[0])
        self.cons_queue.put(current_effect)
        
        # Get the actions chosen by the user
        act_map = self.consume_game_effect().get_actions()
        user_acts = act_map.keys()
        self.role2.set_user_actions(act_map)
        for act in user_acts:
            if act_map[act]: 
                self.role2.on_action(act.get_user_action())
            
            handle_act: bool = self.turn(self.role2)
            if not handle_act:
                return handle_act
    
        # Once all actions are completed, communicate turn done to UI
        self.produce_game_effect(GameEffect(PlayerControlStatus.TURN_DONE))
        return True
    
    def turn_action(self, curr_player): 
        act_map = self.consume_game_effect().get_actions()
        user_acts = act_map.keys()
        for act in user_acts:
            if act_map[act]: 
                print("EXECUTING " + act.get_user_action())
                if curr_player == self.role1.get_role():
                    self.role1.on_action(act)
                else: 
                    self.role2.on_action(act) 
                
                self.role1.end_condition()
                self.role2.end_condition()
                result = self.get_players_data()[0][curr_player]['result'].get_value()
                print(self.get_players_data()[0])

                # CHECKING IF LOST
                if (result != "LOST" and result != "WIN"): 
                    # handle_act: bool = self.turn(self.role2)
                    # if not handle_act:
                    #     return handle_act
                    return False
            
        return True
    
    def turn(self, role) -> bool:
        # Get the game effect from UI
        act_effect = self.mock_get_status()

        # End turn if UI says turn done
        if act_effect.get_player_control_status() == PlayerControlStatus.TURN_DONE:
            return True
        
        # End game if UI forces quit
        if act_effect.get_player_control_status() == PlayerControlStatus.QUIT:
            return False

        # If end game state is reached, communicate Winner or Loser to UI 
        if role.end_condition:
            self.produce_game_effect(GameEffect(PlayerControlStatus.LOSER))
            end_effect = self.consume_game_effect()
            # UI should return QUIT status on winner or looser. Throw error otherwise
            if end_effect.get_player_control_status() == PlayerControlStatus.QUIT:
                return False
            else:
                return NotImplementedError
        return True

    def produce_game_effect(self, game_effect:GameEffect):
        self.prod_queue.put(game_effect)

    def dequeue_next(self) -> GameEffect:
        return self.prod_queue.get()

    def consume_game_effect(self) -> GameEffect:
        poppedEffect = copy.deepcopy(self.cons_queue.get())
        return poppedEffect
    
    def setup_queue(self):
        for role in self.roles:
            self.produce_game_effect(role.setup())
    
    def mock_get_status(self):
       return GameEffect(PlayerControlStatus.QUIT)
   
    def get_players_data(self):
        return [role.get_local_vars() for role in self.roles]

    def get_players(self):
        return self.roles




"""
Call role1 on turn 
Get back game effect
Append game effect to queue for frontend
Get game effect back from frontend
Call the appropriate on action callback
Check end state
If end state -> Add new game effect to queue with  Player control status -> TURN_DONE
Call role2 on turn
"""
