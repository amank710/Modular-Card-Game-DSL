from src.factory.function_context.expressions.expression import Expression


class ConstantExpression(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value
    
    def get_value(self):
        return self.value

    # hey sorry but we should not return like "CONST: self.value" because 
    # it will affect get_corresponding_system_function 
    def __repr__(self) -> str:
        return "CONST: " + str(self.value)
