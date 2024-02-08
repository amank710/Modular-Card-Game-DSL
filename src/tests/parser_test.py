from antlr4 import *
from Tokens import Tokens
from Grammar import Grammar
import unittest

class TestGameParser(unittest.TestCase):
    def test_basic(self): 
        with open("test.txt", "r") as expected_file:
            expected_output = expected_file.read().strip()

        # Process the input file and generate the parse tree
        input_stream = FileStream("input.txt")
        lexer = Tokens(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = Grammar(token_stream)
        tree = parser.program()  # Make sure 'program' is your actual entry point

        # Convert the tree to a string and compare it to the expected output
        actual_output = tree.toStringTree(recog=parser).strip()
        print(actual_output)
        # print("\n")
        print(expected_output)
        
        self.assertEqual(actual_output, expected_output)


def suite():
    suite = unittest.TestSuite() 
    suite.addTest(TestGameParser('test_basic'))
    return suite

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite())