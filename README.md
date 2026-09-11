# CS-1110/MAT-2203 Discrete Mathematics — Assignment 1

**Student:** Saksham Maggo  
**Computational exercises:** Questions 2 and 3

## Files

### `q2_logic_checker.py`
Checks Question 2 by direct enumeration.

There are 3 possible jewel locations and 2 possible kinds for each of the 4 inhabitants, so the program checks

`3 × 2^4 = 48`

possible worlds.

It:
- finds the unique world satisfying all four speeches;
- removes one speech at a time and checks whether uniqueness is lost.

No external package is needed.

### `q2_sat_unsat.py`
A second check for Question 2 using Z3.

The puzzle is encoded as Boolean constraints. The program checks:
- that the complete puzzle is SAT;
- that no second satisfying solution exists;
- Jade, Onyx and Amber by forcing each location in turn;
- the opposite kind for each inhabitant.

The uniqueness test blocks the first solution and asks Z3 for another one. Z3 returns UNSAT, confirming that the solution is unique.

External package needed: `z3-solver`.

### `q3_decision_tree.py`
Checks the questioning problem from Question 3.

It:
- checks the nested-question idea from part (a);
- checks the one-question impossibility from part (b);
- checks the answer pairs from part (c);
- searches for an adaptive decision tree in part (d);
- confirms that 1 and 2 plain questions are insufficient, while 3 are sufficient;
- tests the resulting tree on all 6 possible hidden states;
- runs a small experiment for larger numbers of vaults.

No external package is needed.

## Requirements

Python 3 is required.

Install the only external dependency with:

```bash
python3 -m pip install -r requirements.txt
```

## Running the programs

On macOS/Linux:

```bash
python3 q2_logic_checker.py
python3 q2_sat_unsat.py
python3 q3_decision_tree.py
```

On Windows, use `python` or `py` instead of `python3` if needed.

## Main expected results

For Question 2:

- Jewel: Amber
- Athena: Oracle
- Boreas: Chimera
- Cronus: Oracle
- Demeter: Chimera
- After blocking the first Z3 solution: UNSAT

For Question 3:

- 1 plain question: impossible
- 2 plain questions: impossible
- 3 plain questions: possible
- Decision tree check: correct on all 6 hidden states

## Test status

The direct Question 2 checker and the Question 3 decision-tree program were run successfully with Python 3.  
The Z3 program was also run successfully in Google Colab after installing `z3-solver`.
