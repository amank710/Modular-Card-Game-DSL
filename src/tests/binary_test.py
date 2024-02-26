from factory.function_context.expressions.binary_expression import BinaryExpression
from factory.function_context.expressions.constant_expression import ConstantExpression

import unittest

class TestBinaryExpression(unittest.TestCase):

    def test_basic_binary_expression(self):
        cons_express_ten = ConstantExpression(10)
        cons_express_eleven = ConstantExpression(11)
        bin_express = BinaryExpression('<', cons_express_ten, cons_express_eleven)
        assert bin_express.evaluate() == True

    def test_basic_binary_expression_string(self):
        cons_express_solid = ConstantExpression('solid')
        cons_express_liquid = ConstantExpression('liquid')
        # 'solid' == 'liquid'
        bin_express_2 = BinaryExpression('==', cons_express_solid, cons_express_liquid)
        assert bin_express_2.evaluate() == False

    def test_complex_binary_expression_false(self):
        cons_express_ten = ConstantExpression(10)
        cons_express_eleven = ConstantExpression(11)
        # 10 < 11
        bin_express = BinaryExpression('<', cons_express_ten, cons_express_eleven)

        cons_express_solid = ConstantExpression('solid')
        cons_express_liquid = ConstantExpression('liquid')
        # 'solid' == 'liquid'
        bin_express_2 = BinaryExpression('==', cons_express_solid, cons_express_liquid)

        # 10 < 11 and 'solid' == 'liquid'
        bin_express_final = BinaryExpression('and', bin_express, bin_express_2)
        assert bin_express_final.evaluate() == False



    def test_complex_binary_expression_true(self):
        cons_express_ten = ConstantExpression(10)
        cons_express_eleven = ConstantExpression(11)
        # 10 < 11
        bin_express = BinaryExpression('<', cons_express_ten, cons_express_eleven)

        cons_express_solid = ConstantExpression('solid')
        cons_express_solid2 = ConstantExpression('solid')
        # 'solid' == 'solid'
        bin_express_2 = BinaryExpression('==', cons_express_solid, cons_express_solid2)

        # 10 < 11 and 'solid' == 'solid'
        bin_express_final = BinaryExpression('and', bin_express, bin_express_2)
        assert bin_express_final.evaluate() == True

    def test_complex_binary_expression_or(self):
        cons_express_ten = ConstantExpression(10)
        cons_express_eleven = ConstantExpression(11)
        # 10 >= 11
        bin_express = BinaryExpression('>=', cons_express_ten, cons_express_eleven)

        cons_express_solid = ConstantExpression('solid')
        cons_express_solid2 = ConstantExpression('solid')
        # 'solid' == 'solid'
        bin_express_2 = BinaryExpression('==', cons_express_solid, cons_express_solid2)

        # 10 >= 11 or 'solid' == 'solid'
        bin_express_final = BinaryExpression('or', bin_express, bin_express_2)
        assert bin_express_final.evaluate() == True


    def test_complex_binary_expression_double_and(self):
        cons_express_ten = ConstantExpression(10)
        cons_express_eleven = ConstantExpression(11)
        # 10 != 11
        bin_express = BinaryExpression('!=', cons_express_ten, cons_express_eleven)

        cons_express_solid = ConstantExpression('solid')
        cons_express_solid2 = ConstantExpression('solid')
        # 'solid' == 'solid'
        bin_express_2 = BinaryExpression('==', cons_express_solid, cons_express_solid2)

        cons_express_80 = ConstantExpression(80)
        cons_express_80_2 = ConstantExpression(80)
        # 80 == 80
        bin_express_3 = BinaryExpression('==', cons_express_80, cons_express_80_2)

        # 10 != 11 and 'solid' == 'solid'
        bin_express_penultimate = BinaryExpression('and', bin_express, bin_express_2)

        # 10 != 11 and 'solid' == 'solid' and 80 == 80
        bin_express_final = BinaryExpression('and', bin_express_penultimate, bin_express_3)

        assert bin_express_final.evaluate() == True