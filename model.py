"""
Module with Model API realization
"""
from dataclasses import dataclass, field
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, LpStatusOptimal, get_solver
from matplotlib import pyplot as plt
from consts import Signs
import numpy as np


@dataclass
class Expression:
    """
    Class of the Expression.
    Expression can be objective function or inequality for the constraint
    """
    c1: int = None
    c2: int = None
    c3: int = None
    sign: Signs = None

    def sign_expression(self, x1, x2):
        """
        Forming statement of inequality
        :param x1: linear problem variable x1
        :param x2: linear problem variable x2
        :return: returns expression statement with the sign character
        """
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
        """
        Forming string representation of the expression;
        Format: c1 <number>; c2: <number>; c3: <number>; "sign": <sign string>;
        :return: returns string representation of the expression
        """
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
    """
    Class of the Model.
    Model contains data that defines linear programming problem.
    And has methods for solving and displaying graphical solution of the problem.
    """
    sense: LpMaximize | LpMinimize = None
    obj_fun: Expression = None
    constraints: list[Expression] = field(default_factory=lambda: [])
    problem: LpProblem = None
    x1: LpVariable = None
    x2: LpVariable = None

    def solve(self) -> None:
        """
        Function that using pulp+glpk to solve lp problem
        :return: None
        """
        if self.problem is None:
            self.problem = LpProblem("Optimization_problem", sense=self.sense)

            if self.x1 is None:
                self.x1 = LpVariable(name="x1", lowBound=0)
            if self.x2 is None:
                self.x2 = LpVariable(name="x2", lowBound=0)

            self.problem += self.obj_fun.c1 * self.x1 + self.obj_fun.c2 * self.x2 + self.obj_fun.c3

            for constraint in self.constraints:
                self.problem += constraint.sign_expression(self.x1, self.x2)

        self.problem.solve(solver=get_solver("GLPK_CMD", msg=False))

    def print_optimal(self) -> None:
        """
        Prints optimal solution(if it's founded) to the terminal
        :return: None
        """
        if not self._check_if_optimal():
            print("Problem wasn't solved: call Model.solve method or it doesn't have optimal solution")
            return

        print(f"Optimal value is: {self.problem.objective.value()}")
        print(f"x1: {self.x1.value()}; x2: {self.x2.value()}")

    def draw_solution(self) -> None:
        """
        Draws feasible region, optimal solution(if it's found), objective function
        :return: None
        """
        if not self._check_if_optimal():
            print("Problem wasn't solved: call Model.solve method or it doesn't have optimal solution")
            return

        plt.figure()

        plt.title("Feasible region:")
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.grid()

        lim = int(max(map(lambda c: c.c3, self.constraints)) / 2)

        plt.xlim(0, lim)
        plt.ylim(0, lim)

        x1 = np.linspace(-1, lim, 2000)

        constr_n = len(self.constraints)
        d = np.linspace(0, lim, 300)
        ax1, ax2 = np.meshgrid(d, d)

        area = self.constraints[0].sign_expression(ax1, ax2)
        for i in range(1, constr_n):
            area &= self.constraints[i].sign_expression(ax1, ax2)

        plt.imshow(
            (area).astype(int),
            extent=(ax1.min(), ax1.max(), ax2.min(), ax2.max()),
            origin="lower",
            cmap="Greens",
            alpha=0.3
        )

        for i, constr in enumerate(self.constraints):
            plt.plot(x1, (constr.c3 - constr.c1 * x1) / constr.c2, label=f"Constraint {i+1}")

        plt.plot(
            x1,
            (self.problem.objective.value() - self.obj_fun.c1 * x1 - self.obj_fun.c3) / self.obj_fun.c2,
            label="Objective func"
        )
        plt.plot(self.x1.value(), self.x2.value(), marker='o')
        plt.annotate(f"  Optimal Value ({self.x1.value()}; {self.x2.value()})", (self.x1.value(), self.x2.value()))
        plt.legend()
        plt.show()

    def _check_if_optimal(self) -> bool:
        """
        Checking if optimal solution were found
        :return: returns True if optimal solution were found
        """
        return self.problem and self.problem.status == LpStatusOptimal

    def __str__(self) -> str:
        """
        Forming string representation of the Model;
        :return: returns string representation of the Model;
        """
        constraints_str = "\n\t\t- ".join(map(lambda constraint: str(constraint), self.constraints))
        return f"Model:\n\tSense: {self.sense} \n\tFun: {self.obj_fun} \n\tConstraints:\n\t\t- {constraints_str}"
