from model import Model, Expression
from pulp import LpMinimize, LpMaximize
from typing import Callable
from consts import ParsingConsts, ParsingTypes


def parse_model(path: str) -> Model:
    model = Model()

    with open(path, "r") as md_data:
        problem_tag = md_data.readline()

        if problem_tag.find(ParsingTypes.PROBLEM_TAG.value) == -1:
            raise Exception("Wrong file. Model files should start with \"Problem:\" tag")

        for line in md_data:
            if line.find(ParsingTypes.SENSE.value) != -1:
                model.sense = parse_sense(line)
            if line.find(ParsingTypes.OBJ_FUN.value) != -1:
                model.obj_fun = parse_obj_fun(line)
            if line.find(ParsingTypes.CONSTRAINT.value) != -1:
                model.constraints.append(parse_constraint(line))

    return model


def parse_sense(line: str) -> LpMinimize | LpMaximize:
    return ParsingConsts.SenseTranslator[
        line.strip()
            .removeprefix(ParsingTypes.SENSE.value)
            .removesuffix(";")
            .strip()
    ]


def parse_obj_fun(line: str) -> Expression:
    expr = parse_expression(line.strip().removeprefix(ParsingTypes.OBJ_FUN.value))
    return expr


def parse_constraint(line: str) -> Expression:
    expr = parse_expression(line.strip().removeprefix(ParsingTypes.CONSTRAINT.value))
    return expr


def parse_expression(line: str) -> Expression:
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
    value = token.strip().removeprefix(prefix).removesuffix(suffix).strip()
    return converter(value)
