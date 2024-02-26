from factory.function_context.expressions.binary_expression import BinaryExpression
from factory.function_context.expressions.constant_expression import ConstantExpression
from factory.function_context.expressions.arithmetic_expression import ArithmeticExpression

import unittest

from factory.function_context.expressions.variable_expression import VariableExpression
from game.objects.variable import Variable


class TestArithmeticExpression(unittest.TestCase):

    def test_basic_arithmetic_expression(self):
        cons_express_ten = ConstantExpression(10)
        cons_express_eleven = ConstantExpression(11)
        bin_express = ArithmeticExpression('+', cons_express_ten, cons_express_eleven)
        assert bin_express.evaluate() == 21

    def test_complex_arithmetic_expression(self):
        # variable = Variable(name='score')
        # variable.set_value(10)
        # dict = {
        #     "PLAYER": variable
        # }
        # var_express_ten = VariableExpression(dict, "score", "PLAYER")
        cons_express_five = ConstantExpression(5)
        cons_express_eleven = ConstantExpression(11)
        cons_express_two = ConstantExpression(2)
        # 5 - 11
        ar_express = ArithmeticExpression('-', cons_express_five, cons_express_eleven)
        # (5 - 11) * 2
        ar_express_final = ArithmeticExpression('*', ar_express, cons_express_two)
        assert ar_express_final.evaluate() == -12

    def test_arithmetic_with_binary(self):
        cons_express_five = ConstantExpression(5)
        cons_express_eleven = ConstantExpression(11)
        cons_express_two = ConstantExpression(2)
        cons_express_zero = ConstantExpression(0)
        # 5 - 11
        ar_express = ArithmeticExpression('-', cons_express_five, cons_express_eleven)
        ar_express_final = ArithmeticExpression('*', ar_express, cons_express_two)
        bin_express = BinaryExpression('<', ar_express_final, cons_express_zero)
        assert bin_express.evaluate() == True