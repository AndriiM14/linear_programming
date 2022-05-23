from model import Model, Signs
from math import inf
from prettytable import PrettyTable
from pulp import LpMaximize


def simplex_solver(model: Model) -> None:
    """
    :param model: Model that needs to be solved
    :return: doesn't return anything, it's just printing the result
    """

    # Defining vector of coefficients for x1 and x2
    x1 = []
    x2 = []

    for constraint in model.constraints:
        x1.append(constraint.c1)
        x2.append(constraint.c2)

    # Transforming to canonical
    x = []

    for index, constraint in enumerate(model.constraints):
        if constraint.sign == Signs.GT or constraint.sign == Signs.GTE:
            x.append([-1 if i == index else 0 for i in range(0, len(model.constraints))])
        elif constraint.sign == Signs.LW or constraint.sign == Signs.LWE:
            x.append([1 if i == index else 0 for i in range(0, len(model.constraints))])

    def check_for_base_vec(vec_, index_):
        for i__, v__ in enumerate(vec_):
            if index_ == i__ and v__ != 1:
                return False
            elif index_ != i__ and v__ != 0:
                return False

        return True

    def check_for_base():
        vects__ = [x1, x2, *x]

        for i__ in range(0, len(model.constraints)):
            found__ = False
            for v__ in vects__:
                if check_for_base_vec(v__, i__):
                    found__ = True
                    break

            if not found__:
                return False

        return True

    # Defining var for the base of the solution
    base = []

    # Looking for a need of artificial vars
    a = []

    if not check_for_base():
        vects = [x1, x2, *x]
        for i_ in range(0, len(model.constraints)):
            found = False

            for v in vects:
                if check_for_base_vec(v, i_):
                    found = True
                    break

            if not found:
                a.append([1 if i__ == i_ else 0 for i__ in range(0, len(model.constraints))])

    var_names = ["x1", "x2"]
    obj_fun_coefficients = [model.obj_fun.c1, model.obj_fun.c2]

    for i, _ in enumerate(x):
        var_names.append(f"x{3 + i}")
        obj_fun_coefficients.append(0)

    for i, _ in enumerate(a):
        var_names.append(f"y{1+i}")
        obj_fun_coefficients.append(-inf)

    # Filling base

    vects = [x1, x2, *x, *a]
    for index in range(0, len(model.constraints)):
        for i_, v in enumerate(vects):
            if check_for_base_vec(v, index):
                # base data format is a tuple of  (var_name, coefficient, b value)
                base.append((var_names[i_], obj_fun_coefficients[i_], model.constraints[index].c3))

    table = []
    for index in range(0, len(model.constraints)):
        table.append([])

        for v in vects:
            table[index].append(v[index])

    def print_simplex_table(base_, table_, res_=None):
        p_table = PrettyTable()

        p_table.add_column("base", [name for name, _, _ in base_])
        p_table.add_column("c_base", [c for _, c, _, in base_])
        p_table.add_column("plan", [plan for _, _, plan, in base_])

        for i, name in enumerate(var_names):
            p_table.add_column(name, [row_[i] for row_ in table_])

        if res_ is not None:
            res_m, res_a, opt_val, opt_val_a = res_
            p_table.add_row(["", "m+1", opt_val, *res_m])

            if len(res_a) > 0:
                p_table.add_row(["", "m+2", opt_val_a, *res_a])

        print(p_table)

    def calc_res(base_, table_):
        _res_m = []
        _res_a = []
        _opt_val = 0.
        _opt_val_a = 0.

        for _, c_, p_ in base_:
            if c_ == -inf:
                _opt_val_a += -1 * p_
            else:
                _opt_val += c_ * p_

        for i__, _ in enumerate(vects):
            sum_ = 0.
            sum_a = 0.
            add_to_a = False

            for r__, (_, c_, p_) in enumerate(base_):
                if c_ == -inf:
                    add_to_a = True
                    sum_a += -1 * table_[r__][i__]
                else:
                    sum_ += c_ * table_[r__][i__]

            sum_ -= obj_fun_coefficients[i__]

            if add_to_a:
                _res_a.append(sum_a)
            _res_m.append(sum_)

        return _res_m, _res_a, _opt_val, _opt_val_a

    def check_if_optimal(res_) -> bool:
        _res_m, _res_a, _, _ = res_

        if (len(_res_a) > 0):
            return min(_res_a) >= 0 if model.sense == LpMaximize else max(_res_a) <= 0
        return min(_res_m) >= 0 if model.sense == LpMaximize else max(_res_m) <= 0

    while True:
        res = calc_res(base, table)
        res_m, res_a, opt_val, _ = res
        print_simplex_table(base, table, res)

        if check_if_optimal(res):
            print(f"Solution founded: {opt_val}")
            return

        col = res_a.index(min(res_a) if model.sense == LpMaximize else max(res_a)) if len(res_a) > 0 else res_m.index(min(res_m) if model.sense == LpMaximize else max(res_m))

        if not max([table[r][col] for r in range(len(table))]) > 0:
            print("Model can't be solved")
            return

        ar = []
        for r in range(len(table)):
            if table[r][col] > 0:
                ar.append(base[r][2] / table[r][col])
            else:
                ar.append(inf)

        row = ar.index(min(ar))

        el = table[row][col]

        for r in range(len(base)):
            if r != row:
                base[r] = (base[r][0], base[r][1], (base[r][2] * el - base[row][2] * table[r][col]) / el)
        base[row] = (var_names[col], obj_fun_coefficients[col], base[row][2] / el)

        table_cpy = []
        for r in table:
            table_cpy.append(r[::])

        for r in range(len(table)):
            for c in range(len(table[r])):
                if r == row:
                    table[r][c] /= el
                else:
                    table[r][c] = (table_cpy[r][c] * el - table_cpy[r][col] * table_cpy[row][c]) / el






