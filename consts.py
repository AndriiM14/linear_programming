from enum import Enum
from pulp import LpMaximize, LpMinimize


class Signs(Enum):
    GT = "gt"
    LW = "lw"
    EQ = "eq"
    GTE = "gte"
    LWE = "lwe"


class ParsingConsts:
    SenseTranslator = {
        "MIN": LpMinimize,
        "MAX": LpMaximize
    }

    SignTranslator = {
        "gt": Signs.GT,
        "gte": Signs.GTE,
        "lw": Signs.LW,
        "lwe": Signs.LWE,
        "eq": Signs.EQ
    }

    @staticmethod
    def from_str_to_sign(sign: str) -> Signs:
        return ParsingConsts.SignTranslator[sign]

    class ExpressionTokens(Enum):
        C1 = "c1:"
        C2 = "c2:"
        C3 = "c3:"
        SIGN = "sign:"


class ParsingTypes(Enum):
    PROBLEM_TAG = "Problem:"
    SENSE = "Sense:"
    OBJ_FUN = "Fun:"
    CONSTRAINT = "Constraint:"
