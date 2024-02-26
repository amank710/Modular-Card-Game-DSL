import sys
import threading

import pygame
from random import randint
from ecs import render_system as rs
from ecs import world_system as ws
from src.factory.factory import Factory
from src.tests.util import get_ast, get_parse_tree
from src.dsl_ast.variables_checker_visitor import *

pygame.init() 

# Setting and creating game window
SCREEN_WIDTH = rs.SCREEN_WIDTH
SCREEN_HEIGHT = rs.SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

try:
    tree = get_ast(get_parse_tree(file_path="input.txt"))
    # Continue with the rest of your program if parsing succeeds
except Exception as e:
    print(e)
    sys.exit(1)

checker = VariablesCheckerVisitor()
errors = checker.check(tree)
if errors:
    # Print all errors
    for error in errors:
        print(error)
    # Exit the program with a non-zero exit code to indicate failure
    sys.exit(1)

f = Factory(ast=tree)
game = f.build_game()
game.setup_queue()
if __name__ == "__main__":
    game_thread = threading.Thread(target=game.turn_manager) 
    game_thread.start()
    world_system = ws.WorldSystem(gui_in_queue=game.prod_queue, gui_out_queue=game.cons_queue, players=game.get_players())
    world_system.run()
