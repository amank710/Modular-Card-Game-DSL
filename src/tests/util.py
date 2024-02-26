from src.dsl_ast.ast_generator_visitor import AstVisitorGenerator
from src.dsl_ast.ast_node import ProgramNode
from src.parser.Grammar import Grammar
from src.parser.Tokens import Tokens

from antlr4 import CommonTokenStream, FileStream
from pathlib import Path

from src.tests.TestErrorListener import TestErrorListener


def get_parse_tree(file_path: str) -> Grammar.ProgramContext:
    dir_path = Path(__file__).parent
    full_path = dir_path / file_path
    input_stream = FileStream(full_path)
    lexer = Tokens(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = Grammar(token_stream)

    parser.removeErrorListeners()  # Remove default error listeners
    error_listener = TestErrorListener()
    parser.addErrorListener(error_listener)

    tree = parser.program()

# Check for parsing errors and handle them
    if error_listener.hasErrors():
        print("Parsing errors encountered:")
        for error in error_listener.getErrors():
            print(error)
        raise Exception("Parsing failed due to syntax errors.")  # Or handle as needed

    return tree

    # program() is entry point to the tree
    # return parser.program()


def get_ast(parse_tree_root: Grammar.ProgramContext) -> ProgramNode:
    return AstVisitorGenerator().visitProgram(ctx=parse_tree_root)
