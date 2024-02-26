from src.factory.function_context.expressions.expression import Expression

from enum import Enum

class Relation(str, Enum):
    LESS_THAN = '<'
    GREATER_THAN = '>'
    EQUAL = '=='
    NOT_EQUAL = '!='
    GREATER_THAN_EQUAL_TO = '>='
    LESS_THAN_EQUAL_TO = '<='
    AND = 'and'
    OR = 'or'


class BinaryExpression(Expression):
    def __init__(self, relation, left: Expression, right: Expression):
        super(BinaryExpression, self).__init__()

        self.relation = relation
        self.left = left
        self.right = right

    def evaluate(self):
        if self.relation == Relation.LESS_THAN:
            return self.left.evaluate() < self.right.evaluate()
        elif self.relation == Relation.GREATER_THAN:
            return self.left.evaluate() > self.right.evaluate()
        elif self.relation == Relation.EQUAL:
            return self.left.evaluate() == self.right.evaluate()
        elif self.relation == Relation.NOT_EQUAL:
            return self.left.evaluate() != self.right.evaluate()
        elif self.relation == Relation.GREATER_THAN_EQUAL_TO:
            return self.left.evaluate() >= self.right.evaluate()
        elif self.relation == Relation.LESS_THAN_EQUAL_TO:
            return self.left.evaluate() <= self.right.evaluate()
        elif self.relation == Relation.AND:
            return self.left.evaluate() and self.right.evaluate()
        elif self.relation == Relation.OR:
            return self.left.evaluate() or self.right.evaluate()
        else:
            raise ValueError("[BinaryExpression] Unable to interpret {}".format(str(self.relation)))

    def __repr__(self) -> str:
        return "BINARY ({} {} {})".format(str(self.left), self.relation, str(self.right))
