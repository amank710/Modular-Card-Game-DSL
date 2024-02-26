from src.dsl_ast.ast_node import AstNode
from src.dsl_ast.ast_generator_visitor import AstVisitorGenerator
# from dsl_ast.ast_generator_vistor import AstVisitorGenerator
from src.factory.factory import Factory
from src.parser.Tokens import Tokens
from src.parser.Grammar import Grammar

from antlr4 import CommonTokenStream, FileStream
import argparse
from enum import Enum


class GameMode(Enum):
    CLI = 0


class GameRunner:
    def __init__(self, mode: GameMode, path: str) -> None:
        self.ast: AstNode = self._parse_input(path)

    def _parse_input(self, game_path: str) -> AstNode:
        input_stream = FileStream(game_path)
        lexer = Tokens(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = Grammar(token_stream)

        # TODO: Run through the Static Checker before running the program
        return AstVisitorGenerator().visitProgram(parser.program())

    def build(self) -> None:
        factory = Factory(ast=self.ast)
        factory.build_game()

    def run(self) -> None:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='mcu: the MCU Card Universe',
        description='A Card Game Universe'
    )
    parser.add_argument("game", help="an input .game file")

    args = parser.parse_args()

    game_runner = GameRunner(mode=GameMode.CLI, path="tests/input.txt")
    game_runner.build()
    game_runner.run()
