# Maintainer:     Ryan Young
# Last Modified:  Jan 09, 2022
import numpy as np
from scipy.optimize import linprog

"""

This is a wrapper that makes scipy's linear programming function act like Solver
In other words, this is the closest thing to excel solver in python that exists.

"""

def errors(obj, c_l, c_r, signs, problem_type):
    """
    Helps debug common errors in user code.
    Returns True if any errors present.
    """
    errors = 0
    # ---------------------

    if not len(obj) == len(c_l[0]):
        print(f"Your objective function has {len(obj)} coefficients, but you passed {len(c_l[0])} coefficients in your constraints matrix (c_l).")
        errors += 1

    if not len(c_l) == len(c_r) == len(signs):
        print("The lengths of your c_l, c_r, and signs arrays must be equal.")
        errors += 1

    if not (problem_type == "max" or problem_type == "min"):
        print("Please choose 'max' or 'min' for the problem type")
        errors += 1
    
    if ">" in signs or "<" in signs:
        print("Use of '<' and '>' prohibited. Use '<=' or '>=' instead.")
        errors += 1

    # ---------------------
    if errors > 0:
        return True
    return False


def print_objective_function(obj, problem_type):
    """
    Example:
        (given: [16, -20.5, 14]) output:
        --------------------------------
        MINIMIZE: z = 16a - 20.5b + 14c
        --------------------------------
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    print('------------------------------------------------------')

    if problem_type == "max":
        print("MAXIMIZE: z = ", end="")
    elif problem_type == "min":
        print("MINIMIZE: z = ", end="")

    if obj[0].is_integer():
        print(f"{int(obj[0])}a", end="")
    else:
        print(f"{obj[0]}a", end="")
    for i in range(1, len(obj)):
        num = round(obj[i], ndigits=2)
        if num.is_integer():
            num = int(num)
        if num < 0:
            display_num = f"- {num*-1}"
        else:
            display_num = f"+ {num}"
        print(f" {display_num}{alphabet[i]}", end="")

    print('\n------------------------------------------------------')


def print_results(solution, ptype):
    # Print results
    np.set_printoptions(precision=2, suppress=True)
    optimal = round(solution.fun, ndigits=2)
    if optimal % 1 == 0:
        optimal = int(solution.fun)
    # For maximization problem, reverse the sign of optimal value
    optimal = optimal*-1 if ptype == "max" else optimal
    print(f"OPTIMAL VALUE:  {optimal}")
    print("------------------------------------------------------")
    print("QUANTITIES:")

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for i in range(0, len(solution.x)):
        num = round(solution.x[i], ndigits=5)
        if num % 1 == 0:
            print(f"{alphabet[i]}:  {int(num)}")
        else:
            print(f"{alphabet[i]}:  {num}")

    print("------------------------------------------------------")
    # print(f"Iterations: {solution.nit}")
    print(solution.message)
    print("\n")



def solve(problem_type, objective_function, constraints_left, constraints_right, constraints_signs, make_unconstrained_non_negative=True, minimum_for_all=None, maximum_for_all=None, bounds=None, method="simplex"):

    """
    Main function that translates the Solver-like input into a scipy 'linprog()' call.

    Note: The very long parameter names help suggestions in an IDE, and readability in use.
    """

    if errors(objective_function, constraints_left, constraints_right, constraints_signs, problem_type):
        return

    # convert to numpy so we can multiply by scalars
    obj = np.array(objective_function)
    c_l = np.array(constraints_left)
    c_r = np.array(constraints_right)
    signs = np.array(constraints_signs)

    # Pretty-print the objective function
    print_objective_function(obj, problem_type)

    if not bounds:
        # Default bounds array: a 2d array with len(obj) # of rows, where each row is [0, None]
        # Excel translation: by default, enable 'Make Unconstrained Vars Non-Negative'
        bounds = np.repeat([[0, None]], len(obj), axis=0)

        # The "[:,x]" used below sets column x of each row to the given scalar
        if make_unconstrained_non_negative == False:
            bounds[:,0] = None

        if minimum_for_all:
            bounds[:,0] = minimum_for_all

        if maximum_for_all:
            bounds[:,1] = maximum_for_all

        # Convert bounds 2d array to list of tuples
        bounds = [tuple(x) for x in bounds]

    # Reverse coefficient +/- sign for maximization problem
    if problem_type == "max":
        obj *= -1
    
    # Reverse constraint +/- sign where inequality is ">="
    c_r[signs == ">="] *= -1
    c_l[signs == ">="] *= -1

    # Delete all equalities from c_l and c_r. Move them to their own arrays
    if "=" in signs:
        equalities_left = c_l[signs == "="]
        equalities_right = c_r[signs == "="]
        c_l = np.delete(c_l, np.where(signs == "="), 0)
        c_r = np.delete(c_r, np.where(signs == "="), 0)
    else:
        equalities_left = None
        equalities_right = None

    # Solve linear programming problem
    solution = linprog(obj, A_ub=c_l, b_ub=c_r, A_eq=equalities_left, b_eq=equalities_right, bounds=bounds, method=method)

    print_results(solution, problem_type)
    
    return solution
