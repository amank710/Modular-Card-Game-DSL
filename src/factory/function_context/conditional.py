class Conditional:
    # Assume func_statement a function statement that can be executed
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self):
        # Recursively evaluate the expression and return the result
        return self.evaluate_helper(self.expression)

    def evaluate_helper(self, expression):
        # Recursively evaluate the expression and return the result
        if self.isOperator(expression.get_name()):
            left = self.evaluate_helper(expression.children[0])
            right = self.evaluate_helper(expression.children[1])
            return self.switchHelper(expression.get_name(), left, right)
        #else:
        #    if isinstance(expression, VariableNode):
        #        if self.isStringTrue(expression.get_name()):
        #            return True
        #        elif self.isStringFalse(expression.get_name()):
        #            return False
        #        else:
        #            return expression.get_value()
        #    else:
        #        if self.isStringTrue(expression.get_name()):
        #            return True
        #        elif self.isStringFalse(expression.get_name()):
        #            return False
        #        else:
        #            return expression.get_name()

    def isOperator(self, str):
        return str in ['<', '>', '==', '!=', '>=', '<=', 'and', 'or']

    def isStringTrue(self, str):
        return str in ['True', 'true', 'TRUE']

    def isStringFalse(self, str):
        return str in ['False', 'false', 'FALSE']

    def switchHelper(self, str, left, right):
        if str == '<':
            return left < right
        elif str == '>':
            return left > right
        elif str == '==':
            return left == right
        elif str == '!=':
            return left != right
        elif str == '>=':
            return left >= right
        elif str == '<=':
            return left <= right
        elif str == 'and':
            return left and right
        elif str == 'or':
            return left or right
        else:
            raise Exception("Invalid operator")
