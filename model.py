from dataclasses import dataclass, field
from pulp import LpMaximize, LpMinimize
from consts import Signs


@dataclass
class Expression:
    c1: int = None
    c2: int = None
    c3: int = None
    sign: Signs = None

    def __str__(self):
        res = ""

        res += f"c1: {self.c1}; "
        res += f"c2: {self.c2}; "

        if self.c3:
            res += f"c3: {self.c3}; "

        if self.sign:
            res += f"sign: {self.sign}"

        return res


@dataclass
class Model:
    sense: LpMaximize | LpMinimize = None
    obj_fun: Expression = None
    constraints: list[Expression] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        constraints_str = "\n\t\t- ".join(map(lambda constraint: str(constraint), self.constraints))
        return f"Model:\n\tSense: {self.sense} \n\tFun: {self.obj_fun} \n\tConstraints:\n\t\t- {constraints_str}"
