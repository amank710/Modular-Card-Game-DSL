from src.factory.function_context.expressions.expression import Expression

from enum import Enum
import logging

class Operator(str, Enum):
    PLUS = '+'
    MINUS = '-'
    MULTIPLICATION = '*'
    DIVISION = '/'
    MODULO = '%'

class ArithmeticExpression(Expression):
    def __init__(self, operator, left: Expression, right: Expression):
        super(Expression, self).__init__()

        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self):
        #Enum does not work well with is
        if str(self.operator) == Operator.PLUS:  
            return self.left.evaluate() + self.right.evaluate()
        elif self.operator == Operator.MINUS:
            return self.left.evaluate() - self.right.evaluate()
        elif self.operator == Operator.MULTIPLICATION:
            return self.left.evaluate()*self.right.evaluate()
        elif self.operator == Operator.DIVISION: 
            return self.left.evaluate()/self.right.evaluate()
        elif self.operator == Operator.MODULO:
            return self.left.evaluate() % self.right.evaluate()
        else:
            logging.debug("[ArithmeticExpression] Unable to interpret {}".format(str(self.operator)))

    def __repr__(self) -> str:
        return "ARITHMETIC ({} {} {})".format(str(self.left), self.operator, str(self.right))
