from enum import Enum


class FunctionType(str, Enum):
    COMMON = "COMMON"
    USER_OVERRIDE = "USER_OVERRIDE"
    RESULT = "RESULT"
