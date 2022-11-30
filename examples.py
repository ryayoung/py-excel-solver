import solver

solver.solve(
    problem_type = "min",
    objective_function = [
        10, 15, 25
    ],
    constraints_left = [
        [1,  1,  1],
        [1, -2,  0],
        [0,  0,  1],
    ],
    constraints_right = [
        1000,
        0,
        340,
    ],
    constraints_signs = [
        ">=",
        ">=",
        ">=",
    ],
    make_unconstrained_non_negative = True
)

print("Problem #2:")

solver.solve(
    problem_type = "max",
    objective_function = [
        16, 20.5, 14
    ],
    constraints_left = [
        [4,  6,  2],
        [3,  8,  6],
        [9,  6,  4],
        [30, 40, 25],
    ],
    constraints_right = [
        2000,
        2000,
        1440,
        9600,
    ],
    constraints_signs = [
        "<=",
        "<=",
        "<=",
        "<=",
    ],
)

# print("Problem #3:")
solver.solve(
    problem_type = "min",
    objective_function = [
        4, 5, 3, 7, 6
    ],
    constraints_left = [
        [10,  20,  10,  30,  20],
        [5,   7,   4,   9,   2],
        [1,   4,   10,  2,   1],
        [500, 450, 160, 300, 500],
    ],
    constraints_right = [
        16,
        10,
        15,
        600,
    ],
    constraints_signs = [
        ">=",
        ">=",
        ">=",
        ">=",
    ],
    minimum_for_all=0.1,
)

solver.solve(
    problem_type = "max",
    objective_function = [
        16, 20.5, 14
    ],
    constraints_left = [
        [4,  6,  2],
        [9,  6,  4],
        [30, 40, 25],
        [3,  8,  6],
    ],
    constraints_right = [
        2000,
        1440,
        9600,
        1984,
    ],
    constraints_signs = [
        "<=",
        "<=",
        "<=",
        "=",
    ],
)
