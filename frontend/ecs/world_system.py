import logging
import pygame 
import copy
import random
from ecs import render_system as render
from ecs import card_system as cs
from src.game.objects.game_effect import PlayerControlStatus
from src.game.objects.game_effect import GameEffect, PlayerControlStatus
from src.game.objects.game_action import GameAction
from src.game.objects.system_action import SystemAction

logging.getLogger().setLevel(logging.CRITICAL)

class WorldSystem: 
    def __init__(self, gui_in_queue, gui_out_queue, players): 
        self.running = True
        self.game_over = False
        self.turn_states = []
        self.buttons = []
        self.actionDict = {}
        self.actionsArr = []
        self.cards = []
        self.deck_count = 0
        self.hands = {}
        self.current_player = ""
        self.game_effect = GameEffect()
        self.final_dequeue = True
        self.gui_in_queue = gui_in_queue
        self.gui_out_queue = gui_out_queue
        self.players = players

    def load_game_effect(self):
        self.game_effect = self.gui_in_queue.get()

    def set_buttons(self):
        self.buttons = []
        # Game effect/actions buttons
        for i in range(len(self.actionsArr)):
            x_coord = render.SCREEN_WIDTH - (render.x_spacing * (i + 1))
            if i == 0:
                x_coord = render.SCREEN_WIDTH - render.button_width
            currButton = render.Button(
                x_coord,
                0,
                render.button_width,
                render.button_height,
                self.actionsArr[i],
                36)
            self.buttons.append(currButton)

        # end game button
        end_game_button = render.Button(
            render.SCREEN_WIDTH - (render.button_width),
            render.SCREEN_HEIGHT - (render.y_spacing),
            render.button_width,
            render.button_height,
            "End Game",
            26)
        self.buttons.append(end_game_button)

    def set_actions(self):
        self.actionsArr = []

        # Action system initialization here 
        self.actionDict = self.game_effect.get_actions()
        for action in self.actionDict.keys():
            if self.actionDict[action] == False:
                self.actionsArr.append(action.get_user_action())

    def set_cards(self):
        deck = cs.Deck()
        deck.load_images()
        self.cards = deck.create_deck()
        self.deck_count = len(self.cards)

    def add_player(self, player):
        self.hands[player] = []
        self.current_player = player
        self.turn_states.append(player)

    def end_turn(self):
        for turn in self.turn_states:
            if self.current_player != turn:
                self.current_player = turn
                break

        self.set_actions()
        self.send_to_game()

    def doSystemAction(self, system_action):
        if (system_action.value == "PICK CARD"):
            # Pick a interacting card from PickCard action
            card = system_action.get_value()
            self.hands[self.current_player].append(self.cards[card])
            self.deck_count -= 1
            #print("Role: " + self.current_player.get_role())
            #print("Cards:")
            score = 0
            for val in self.hands[self.current_player]:
                #print(val.get_card_value())
                score += val.get_card_value()
            #print("Total",score)

    def endGame(self):

        # Use first player (0 player is global) to determine who won the game
        # This is because we evaluate PLAYER role first on our DSL.
        player = list(self.game.get_players_data()[0].keys())[1]
        result = self.game.get_players_data()[0][player]['result'].get_value()
        if result == "WIN":
            self.game_effect.set_player_control_status(PlayerControlStatus.WINNER)
        elif result == "LOST":
            self.game_effect.set_player_control_status(PlayerControlStatus.LOSER)

        print("GAME OVER")
        self.game_over = True

    def send_to_game(self):
        self.gui_out_queue.put(self.game_effect)

    def check_game_over(self):
        status = self.game_effect.get_player_control_status()
        if status == PlayerControlStatus.IN_PROGRESS or status == PlayerControlStatus.UNKNOWN or status == PlayerControlStatus.TURN_DONE:
            return False

        return True

    def check_end_turn(self):
        status = self.game_effect.get_player_control_status()
        if self.check_game_over() or status == PlayerControlStatus.TURN_DONE:
            return True

        return False

    def button_function(self, text):
        if text == "End Game":
            self.game_effect.set_player_control_status(PlayerControlStatus.QUIT)
            self.send_to_game()
            self.endGame()
            return

        actionDict = self.game_effect.get_actions()
        for action in actionDict: 
            actionStr = action.get_user_action()
            if (actionStr == text):
                actionDict[action] = True

        self.send_to_game()


    def render_game(self):
        pygame.init()
        # Config
        screen = pygame.display.set_mode((render.SCREEN_WIDTH, render.SCREEN_HEIGHT))
        pygame.display.set_caption(render.gameName)

        # This can be the program/game name 
        gameName = "MY OWN CARD GAME!"
        pygame.display.set_caption(gameName)

        # Card back creation
        card_back = cs.Card("", "", "")
        card_back.shown = False

        while(self.running):
            screen.fill(render.GREY)

            if self.check_game_over():
                self.game_over = True

            if not self.gui_in_queue.empty():
                actionDict = self.game_effect.get_actions()
                for action in actionDict.keys(): 
                    if actionDict[action]: 
                        self.doSystemAction(action.get_system_action()[0])

                self.load_game_effect()

                logging.info("[GUI] Loaded Game Effect {}".format(self.game_effect))
                if self.check_end_turn():
                    logging.info('[GUI] Ending turn for current player: {}'.format(self.current_player.get_role()))
                    self.end_turn()
                else :
                    self.set_actions()
                    self.set_buttons()

                logging.info("[GUI] num actions: {}, num buttons: {}".format(len(self.buttons), len(self.actionsArr)))

            for button in self.buttons: 
                button.draw(screen)
                button.setAction(self.button_function)

            x = render.x_card  + cs.CARD_MAX_WIDTH
            y = render.y_card
            # Loop through some representation of hand here:
            player = list(self.hands.keys())[0]
            currentIndex = 0
            otherPlayer = 1
            if (player != self.current_player):
                currentIndex = 1
                otherPlayer = 0

            for card in self.hands[list(self.hands.keys())[currentIndex]]:
                card.createCard(x, y - 60, screen)
                x += cs.CARD_MAX_WIDTH + 10

            otherX = render.x_card + cs.CARD_MAX_WIDTH
            for card in self.hands[list(self.hands.keys())[otherPlayer]]:
                card.createCard(otherX, y + cs.CARD_MAX_HEIGHT + 25, screen, scale=0.75)
                otherX += cs.CARD_MAX_WIDTH

            # Card back static rendering
            card_back.createCard(0,  render.SCREEN_HEIGHT/2 - cs.CARD_MAX_HEIGHT/2 -70, screen)

            deck_count_str = "Deck Count: " + str(self.deck_count)
            turn_deck_count = render.Turn(20, deck_count_str, render.button_width, 24, 0,
                                          render.SCREEN_HEIGHT/2 - cs.CARD_MAX_HEIGHT/2 - 100)

            turn_deck_count.drawTurnMarker(screen)
            pygame.draw.line(screen, (0, 0, 0), (0, render.SCREEN_HEIGHT / 2), (render.SCREEN_WIDTH, render.SCREEN_HEIGHT / 2), 5)
            current_score = self.game_effect.get_score()
            if current_score is not None:
                turn_marker = render.Turn(24, "Current Turn: " + str(self.current_player.get_role()),
                                      render.button_width + 100, render.button_height, 0, 10)
                turn_marker.drawTurnMarker(screen)
            score_marker = render.Turn(24, "Score: " + str(current_score),
                                       render.button_width, render.button_height, 0, 34)

            score_marker.drawTurnMarker(screen)

            otherPlayerLabel = render.Turn(20, "Previous Turn: "  + str(list(self.hands.keys())[otherPlayer].get_role()), render.button_width + 60, 20, 0,
                                           render.SCREEN_HEIGHT/ 2 +10)

            card_back.createCard(0,  render.SCREEN_HEIGHT/2 - cs.CARD_MAX_HEIGHT/2 + 200, screen)

            deck_count_str = "Deck Count: " + str(self.deck_count)
            turn_deck_count = render.Turn(20, deck_count_str, render.button_width, 20, 0,
                                          render.SCREEN_HEIGHT/ 2 + 70)
            turn_deck_count.drawTurnMarker(screen)


            otherPlayerLabel.drawTurnMarker(screen)

            x += cs.CARD_MAX_WIDTH + 50

            # Event Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in self.buttons:
                    button.handle_event(event)

            # Handle if Game is Over
            if self.game_over:
                screen.fill(render.BLACK)

                # if (self.final_dequeue):
                #     self.game_effect = self.game.dequeue_next() 
                #     self.set_actions()
                #     self.final_dequeue = False

                actualCurrent = "placeholder"
                for player in self.hands.keys():
                    if (player != self.current_player):
                        actualCurrent = player
                is_tie = False

                # WINNER IS NOW OPPOSITE PLAYER SINCE GAME ENDED
                if self.game_effect.get_player_control_status() == PlayerControlStatus.LOSER:
                    loser = actualCurrent.get_role()
                    winner = self.current_player.get_role()
                elif self.game_effect.get_player_control_status() == PlayerControlStatus.WINNER:
                    winner = actualCurrent.get_role()
                    loser = self.current_player.get_role()
                else: 
                    # winner is the uppermost text
                    winner = "It's a tie!"
                    # loser is the bottom text
                    loser = "Neither " + self.current_player.get_role() + " nor " + actualCurrent + " wins!"
                    is_tie = True

                gameOverScreen = render.GameOver(36, winner, loser,
                                                 render.SCREEN_WIDTH, render.SCREEN_HEIGHT,
                                                 is_tie)
                gameOverScreen.drawEndScene(screen)

            # Update screen
            pygame.display.update()

        pygame.quit()

    def run(self):
        #print("RUNNING")
        # for two players' worth of setup functions
        self.load_game_effect()
        self.load_game_effect()

        self.load_game_effect()
        self.set_actions()
        self.set_buttons()

        self.set_cards()
 
        # TODO(arun): remove hack that first player must be added last
        self.add_player(self.players[1])
        self.add_player(self.players[0])

        self.render_game()
