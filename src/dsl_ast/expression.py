from os import access
from src.dsl_ast.ast_node import AstNode
from src.factory.function_context.expressions.arithmetic_expression import ArithmeticExpression
from src.factory.function_context.expressions.binary_expression import BinaryExpression
from src.factory.function_context.expressions.variable_expression import VariableExpression
from src.factory.function_context.expressions.constant_expression import ConstantExpression


class ExpressionNode:
    def __init__(self, name):
        self.name=name

    def createExpression(self, variables_map):
        raise NotImplementedError

class VariableExpressionNode(ExpressionNode):
    def __init__(self, access_context):
        super(VariableExpressionNode, self).__init__(name=access_context.get_name())

        self.role = access_context.get_role()

    def createExpression(self, variables_map):
        return VariableExpression(variables_map=variables_map, var_name=self.name, role=self.role)

class ExpressionValueNode(ExpressionNode):
    def createExpression(self, variables_map):
        return ConstantExpression(value=self.name)

class BinaryExpressionNode(ExpressionNode):
    def __init__(self, name, left: ExpressionNode, right: ExpressionNode):
        super(BinaryExpressionNode, self).__init__(name=name)

        self.left = left
        self.right = right

    def createExpression(self, variables_map):
        return BinaryExpression(relation=self.name, left=self.left.createExpression(variables_map=variables_map),
                         right=self.right.createExpression(variables_map=variables_map))

class ArithmeticExpressionNode(ExpressionNode):
    def __init__(self, operator, left: ExpressionNode, right: ExpressionNode):
        self.operator = operator
        self.left = left
        self.right = right

    def createExpression(self, variables_map):
        return ArithmeticExpression(operator=self.operator,
                                    left=self.left.createExpression(variables_map=variables_map),
                                    right=self.right.createExpression(variables_map=variables_map))
