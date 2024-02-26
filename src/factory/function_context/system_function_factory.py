from src.factory.config import Config
from src.factory.function_context.expressions.expression import Expression
from src.factory.function_context.wait_for_statement import WaitForStatement

from enum import Enum
from typing import List


class SystemFunctionFactory():
    class SystemFunction(str, Enum):
        WAIT_FOR = "waitFor"

    def build(self, func: str, args: List[Expression], config: Config):
        if func == SystemFunctionFactory.SystemFunction.WAIT_FOR:
            return WaitForStatement(args=args, config=config)
