from dataclasses import dataclass, field
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, LpStatusOptimal, get_solver
from consts import Signs


@dataclass
class Expression:
    c1: int = None
    c2: int = None
    c3: int = None
    sign: Signs = None

    def sign_expression(self, x1: LpVariable, x2: LpVariable):
        if self.sign == Signs.GT:
            return self.c1 * x1 + self.c2 * x2 > self.c3
        elif self.sign == Signs.GTE:
            return self.c1 * x1 + self.c2 * x2 >= self.c3
        elif self.sign == Signs.LW:
            return self.c1 * x1 + self.c2 * x2 < self.c3
        elif self.sign == Signs.LWE:
            return self.c1 * x1 + self.c2 * x2 <= self.c3
        elif self.sign == Signs.EQ:
            return self.c1 * x1 + self.c2 * x2 == self.c3

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
    problem: LpProblem = None
    x1: LpVariable = None
    x2: LpVariable = None

    def solve(self) -> None:
        if self.problem is None:
            self.problem = LpProblem("Optimization_problem", sense=self.sense)

            if self.x1 is None:
                self.x1 = LpVariable(name="x1", lowBound=0)
            if self.x2 is None:
                self.x2 = LpVariable(name="x2", lowBound=0)

            self.problem += self.obj_fun.c1 * self.x1 + self.obj_fun.c2 * self.x2

            for constraint in self.constraints:
                self.problem += constraint.sign_expression(self.x1, self.x2)

        self.problem.solve(solver=get_solver("GLPK_CMD", msg=False))

    def print_optimal(self) -> None:
        if not self._check_if_optimal():
            print("Problem wasn't solved: call Model.solve method or it doesn't have optimal solution")
            return

        print(f"Optimal value is: {self.problem.objective.value()}")
        print(f"x1: {self.x1.value()}; x2: {self.x2.value()}")

    def _check_if_optimal(self) -> bool:
        return self.problem and self.problem.status == LpStatusOptimal

    def __str__(self) -> str:
        constraints_str = "\n\t\t- ".join(map(lambda constraint: str(constraint), self.constraints))
        return f"Model:\n\tSense: {self.sense} \n\tFun: {self.obj_fun} \n\tConstraints:\n\t\t- {constraints_str}"
