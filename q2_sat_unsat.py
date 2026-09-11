# Question 2 - SAT / UNSAT using Z3
# Run this once if Z3 is not installed:
# pip install z3-solver

from z3 import Bool, Solver, And, Or, Not, Implies, sat, unsat


# True = Oracle, False = Chimera
athena = Bool("athena")
boreas = Bool("boreas")
cronus = Bool("cronus")
demeter = Bool("demeter")

# chest variables
jade = Bool("jade")
onyx = Bool("onyx")
amber = Bool("amber")


# exactly one chest has the jewel
one_chest = Or(
    And(jade, Not(onyx), Not(amber)),
    And(Not(jade), onyx, Not(amber)),
    And(Not(jade), Not(onyx), amber)
)


# Athena:
# If the jewel is in jade, then I am a chimera.
athena_says = Implies(jade, Not(athena))
athena_rule = (athena == athena_says)


# Boreas:
# Cronus is an oracle only if the jewel is in onyx.
boreas_says = Implies(cronus, onyx)
boreas_rule = (boreas == boreas_says)


# Cronus:
# At least one of Athena and Demeter is a chimera.
cronus_says = Or(Not(athena), Not(demeter))
cronus_rule = (cronus == cronus_says)


# Demeter:
# Boreas and Cronus are of the same kind.
demeter_says = (boreas == cronus)
demeter_rule = (demeter == demeter_says)


rules = [
    one_chest,
    athena_rule,
    boreas_rule,
    cronus_rule,
    demeter_rule
]


def get_bool(model, var):
    return bool(model.eval(var, model_completion=True))


def kind_name(value):
    if value:
        return "Oracle"
    return "Chimera"


def show_solution(model):
    print("Jewel in Jade :", get_bool(model, jade))
    print("Jewel in Onyx :", get_bool(model, onyx))
    print("Jewel in Amber:", get_bool(model, amber))
    print()

    print("Athena :", kind_name(get_bool(model, athena)))
    print("Boreas :", kind_name(get_bool(model, boreas)))
    print("Cronus :", kind_name(get_bool(model, cronus)))
    print("Demeter:", kind_name(get_bool(model, demeter)))


# -------------------------------------------------
# 1. Solve the puzzle
# -------------------------------------------------

s = Solver()
s.add(rules)

ans = s.check()

print("FULL PUZZLE")
print("Result:", ans)
print()

if ans == sat:
    m = s.model()
    show_solution(m)


# -------------------------------------------------
# 2. Check if the solution is unique
# -------------------------------------------------

if ans == sat:
    vars_list = [jade, onyx, amber, athena, boreas, cronus, demeter]

    # ask for another model which differs in at least one variable
    different_solution = Or(*[
        v != m.eval(v, model_completion=True)
        for v in vars_list
    ])

    s.push()
    s.add(different_solution)

    ans2 = s.check()

    print()
    print("UNIQUENESS CHECK")
    print("Result after blocking the first solution:", ans2)

    if ans2 == unsat:
        print("No second solution exists.")
        print("So the solution is unique.")
    else:
        print("Another solution exists:")
        show_solution(s.model())

    s.pop()


# -------------------------------------------------
# 3. Force each chest and check SAT / UNSAT
# -------------------------------------------------

print()
print("CHEST CHECKS")

chest_cases = [
    ("Jade", jade),
    ("Onyx", onyx),
    ("Amber", amber)
]

for name, condition in chest_cases:
    test = Solver()
    test.add(rules)
    test.add(condition)

    result = test.check()
    print(name, "->", result)


# -------------------------------------------------
# 4. Force the opposite person-types
# -------------------------------------------------

print()
print("WRONG TYPE CHECKS")

wrong_types = [
    ("Athena = Chimera", Not(athena)),
    ("Boreas = Oracle", boreas),
    ("Cronus = Chimera", Not(cronus)),
    ("Demeter = Oracle", demeter)
]

for name, condition in wrong_types:
    test = Solver()
    test.add(rules)
    test.add(condition)

    result = test.check()
    print(name, "->", result)
