"""
Module for parsing models from input files
"""
from model import Model, Expression
from pulp import LpMinimize, LpMaximize
from typing import Callable
from consts import ParsingConsts, ParsingTypes


def parse_model(path: str) -> Model:
    """
    Parses file and returns instance of Model
    :param path: the path to the input file
    :return: returns Model parsed from the file
    """
    model = Model()

    with open(path, "r") as md_data:
        problem_tag = md_data.readline()

        """
        Checking if provided file describes problem
        """
        if problem_tag.find(ParsingTypes.PROBLEM_TAG.value) == -1:
            raise Exception("Wrong file. Model files should start with \"Problem:\" tag")

        """
        Going through lines of the file and parsing data for the Model
        """
        for line in md_data:
            if line.find(ParsingTypes.SENSE.value) != -1:
                model.sense = parse_sense(line)
            if line.find(ParsingTypes.OBJ_FUN.value) != -1:
                model.obj_fun = parse_obj_fun(line)
            if line.find(ParsingTypes.CONSTRAINT.value) != -1:
                model.constraints.append(parse_constraint(line))

    return model


def parse_sense(line: str) -> LpMinimize | LpMaximize:
    """
    Translate MIX | MAX into LpMinimize | LpMaximize
    :param line: line from the fie with "Sense:" tag
    :return: returns LpMinimize or LpMaximize const from pulp library
    """
    return ParsingConsts.SenseTranslator[
        line.strip()
            .removeprefix(ParsingTypes.SENSE.value)
            .removesuffix(";")
            .strip()
    ]


def parse_obj_fun(line: str) -> Expression:
    """
    Parses expression for the objective function
    :param line: line from the file with "Fun:" tag
    :return: returns Expression for the objective function
    """
    expr = parse_expression(line.strip().removeprefix(ParsingTypes.OBJ_FUN.value))
    return expr


def parse_constraint(line: str) -> Expression:
    """
    Parses expression for the constraint
    :param line: line from the file with "Constraint:" tag
    :return: returns Expression for the constraint
    """
    expr = parse_expression(line.strip().removeprefix(ParsingTypes.CONSTRAINT.value))
    return expr


def parse_expression(line: str) -> Expression:
    """
    Tokenizes line, extract values, build Expression
    :param line: line to tokenize and get the value from
    :return: returns built Expression
    """
    expr = Expression()

    tokens = line.split(";")
    for token in tokens:
        if token.find(ParsingConsts.ExpressionTokens.C1.value) != -1:
            expr.c1 = extract_value(token, ParsingConsts.ExpressionTokens.C1.value, converter=int)
        if token.find(ParsingConsts.ExpressionTokens.C2.value) != -1:
            expr.c2 = extract_value(token, ParsingConsts.ExpressionTokens.C2.value, converter=int)
        if token.find(ParsingConsts.ExpressionTokens.C3.value) != -1:
            expr.c3 = extract_value(token, ParsingConsts.ExpressionTokens.C3.value, converter=int)
        if token.find(ParsingConsts.ExpressionTokens.SIGN.value) != -1:
            expr.sign = extract_value(token, f"{ParsingConsts.ExpressionTokens.SIGN.value} \"", "\"",
                                      ParsingConsts.from_str_to_sign)

    return expr


def extract_value(token: str, prefix: str = "", suffix: str = "", converter: Callable = str):
    """
    Extracts value from the token and converts to the needed type
    :param token: Token where value will be extracted
    :param prefix: Prefix of the token to remove
    :param suffix: Suffix of the token to remove
    :param converter: Callable object that converts value of type string to needed type
    :return: returns a value of type that converter converts to
    """
    value = token.strip().removeprefix(prefix).removesuffix(suffix).strip()
    return converter(value)
