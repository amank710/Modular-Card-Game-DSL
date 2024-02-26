class Variable:
    INDIRECT_VARIABLE = "_indirect_variable_"
    GLOBAL = "GLOBAL"

    def __init__(self, name):
        self.name = name
        self.value = None

    def get_name(self):
        return self.name

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(self.value)

    def __repr__(self) -> str:
        return "{} = {}".format(self.name, self.value)
