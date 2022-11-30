<h1> py-excel-solver &nbsp;&nbsp;&nbsp; <a href="https://pypi.org/project/excel-solver/" alt="Version"> <img src="https://img.shields.io/pypi/v/excel-solver.svg" /></a> </h1>

A wrapper that uses Scipy's ```linprog()``` function to emulate the UI of Excel's Solver. It's supposed to be extremely easy to use. If you've set up a simple optimization problem in Excel, just copy and paste the values into the function below and get the same output.

<!-- #### [Source code](https://github.com/ryayoung/py-excel-solver) -->

<br>

## Install

```text
pip install excel_solver
```
---

<details>
  <summary><i><b>How to use</b></i></summary>
  
1. Download ```solver.py``` (click 'raw' view, then right click, Save As)
2. ```import solver```, then follow the format of the implementations below
3. Optional: download ```example-code.py``` and execute it from same folder as solver.py to test it out.
  
Params for ```solver.solve()```:
- _problem_type:_ Required. Specify "max" or "min"
- _objective_function:_ Required. List of coefficients.
- _constraints_left:_ Required. Constraint matrix, where columns correspond to objective function coefficients. Can be 2d list or np arr.
- _constraints_right:_ Required. These are constraint vectors used to make the comparison.
- _constraints_signs:_ Required. A list of signs corresponding to your constraints. Allowed: ```>=, <=, =```
- _make_unconstrained_non_negative:_ (optional) Just like the button in Excel. Setting this to False is the same as setting minimum_for_all to None.
- _minimum_for_all:_ (optional) Set the lower limit for all decision variables.
- _maximum_for_all:_ (optional) Set the upper limit for all decision variables.
- _bounds:_ (optional) default None. Use this to specify custom bounds for each var individually. Pass an array of tuples [(), (), etc.].
- _method:_ (optional) default simplex. You can pass any of the ones listed in Scipy documentation.
- _display_result:_ (optional) default True
</details>

<details>
  <summary><i><b>Rules:</b></i></summary>

- All matrix constraints must be able to be stated with a SUMPRODUCT() in Excel. Instead of passing the sumproduct cell as a constraint like you would in Excel, here you need to pass the constraint matrix itself (see ```constraints_left``` param below), and the function will take care of the math.
</details>

<details>
  <summary><i><b>Why use this?</b></i></summary>

- It's easy. Very easy. You can simply copy paste from excel into the function. You even get to use the "Make Unconstrained Variables Non-Negative" button, like you would in Excel.
</details>

<details>
  <summary><i><b>Extra features you don't get in Excel Solver</b></i></summary>
    
- With a single-integer assignment, you can set the ```minimum_for_all``` and/or ```maximum_for_all``` constraints to set an upper and/or lower bound for all the decision variables at once.
- You don't have to calculate objective function or matrix sumproduct constraints yourself.
- Objective function is set up and displayed for you in the output. Ex: ```MINIMIZE: z = 16a - 20.5b + 14c```.
- Choose from a variety of solve methods not offered in Excel.
</details>

<details>
  <summary><i><b>Why not just use scipy.optimize.linprog()?</b></i></summary>

- Scipy's ```linprog()``` is very hard to use if you're coming from Excel. It does NOT let you pick between maximize and minimize like you would in Excel, and it does not let you specify inequality signs (>= <=) for constraints. And, if you want to assert equalities as constraints, you have to pass them as a completely separate matrix/vector pair in the function. As a result, using scipy linprog() requires that you manipulate many of your values ahead of time in a way that makes your code impossible to read and interpret.
</details>


### Example 1
Solved in Excel:
![image](https://user-images.githubusercontent.com/90723578/148739017-b8ee6e72-5684-44d3-aaa0-9dc4d0f905eb.png)

Solved in Python:
#### Code:
```python
import solver
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
    minimum_for_all=0.1, # replaces lines 15-19 in the excel image above
)
```
#### Output:
```
------------------------------------------------------
MINIMIZE: z = 4a + 5b + 3c + 7d + 6e
------------------------------------------------------
OPTIMAL VALUE:  8.04
------------------------------------------------------
QUANTITIES:
a:  0.44415
b:  0.18091
c:  1.35322
d:  0.1
e:  0.1
------------------------------------------------------
Optimization terminated successfully. (HiGHS Status 7: Optimal)

```

### Example 2
Solved in Excel:
![image](https://user-images.githubusercontent.com/90723578/148739337-9335fa73-b1fd-42a5-b7ae-8c1c23382c0d.png)

Solved in Python:
#### Code
```python
import solver
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
```
#### Output
```
------------------------------------------------------
MAXIMIZE: z = 16a + 20.5b + 14c
------------------------------------------------------
OPTIMAL VALUE:  4960
------------------------------------------------------
QUANTITIES:
a:  0
b:  160
c:  120
------------------------------------------------------
Optimization terminated successfully. (HiGHS Status 7: Optimal)
```

#### Now, let's try switching the 2nd constraint in the previous problem from '<= 2000' to '= 1984'. If you were using Scipy, this wouldn't be possible without making two new separate arrays to store this constraint.

NOTE: This is _NOT_ necessary, but I've re-ordered the constraints so the equality is on the bottom. You can have them in any order you like.
#### Code
```python
import solver
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
```
#### Output
```
------------------------------------------------------
MAXIMIZE: z = 16a + 20.5b + 14c
------------------------------------------------------
OPTIMAL VALUE:  4952
------------------------------------------------------
QUANTITIES:
a:  0
b:  176
c:  96
------------------------------------------------------
Optimization terminated successfully. (HiGHS Status 7: Optimal)
```
