"""
Module with consts for parser and model modules
"""
from enum import Enum
from pulp import LpMaximize, LpMinimize


class Signs(Enum):
    """
    Enum of the sign types
    """
    GT = "gt"
    LW = "lw"
    EQ = "eq"
    GTE = "gte"
    LWE = "lwe"


class ParsingConsts:
    """
    Consts for parsing
    """

    """
    Map for translating MIN | MAx to LpMinimize | LpMaximize
    """
    SenseTranslator = {
        "MIN": LpMinimize,
        "MAX": LpMaximize
    }

    """
    Map for translating string signs to Signs enum type
    """
    StrEnumSigns = {
        "gt": Signs.GT,
        "gte": Signs.GTE,
        "lw": Signs.LW,
        "lwe": Signs.LWE,
        "eq": Signs.EQ
    }

    @staticmethod
    def from_str_to_sign(sign: str) -> Signs:
        """
        Callable converter from string sign to Sign enum type
        :param sign: string sings
        :return: returns Sign enum type of provided sign
        """
        return ParsingConsts.StrEnumSigns[sign]

    class ExpressionTokens(Enum):
        """
        Enum with expression tokens to be parsed with parse_expression function
        """
        C1 = "c1:"
        C2 = "c2:"
        C3 = "c3:"
        SIGN = "sign:"


class ParsingTypes(Enum):
    """
    Enum of tags to be parsed
    """
    PROBLEM_TAG = "Problem:"
    SENSE = "Sense:"
    OBJ_FUN = "Fun:"
    CONSTRAINT = "Constraint:"
