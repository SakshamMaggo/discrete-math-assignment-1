# Question 3 - decision tree check

vaults = ["Coral", "Amber", "Topaz"]


# state = (vault number, True/False)
# True means Oracle, False means Chimera

def make_states(n):
    states = []

    for i in range(n):
        states.append((i, True))
        states.append((i, False))

    return states


def answer(state, asked):
    vault, oracle = state

    actual = (vault == asked)

    if oracle:
        return actual
    else:
        return not actual


def nested_answer(state, asked):
    # question of the form:
    # "Is your answer to 'Is the jewel in X?' yes?"

    inside = answer(state, asked)

    if state[1]:          # Oracle
        return inside
    else:                 # Chimera lies again
        return not inside


def same_vault(states):
    v = states[0][0]

    for s in states:
        if s[0] != v:
            return False

    return True


def split(states, asked):
    yes = []
    no = []

    for s in states:
        if answer(s, asked):
            yes.append(s)
        else:
            no.append(s)

    return yes, no


# returns a decision tree if possible, otherwise None
def search(states, qleft, n, memo):
    key = (tuple(sorted(states)), qleft)

    if key in memo:
        return memo[key]

    if same_vault(states):
        tree = ("done", states[0][0])
        memo[key] = tree
        return tree

    if qleft == 0:
        memo[key] = None
        return None

    for asked in range(n):
        yes, no = split(states, asked)

        # useless question
        if len(yes) == 0 or len(no) == 0:
            continue

        ytree = search(yes, qleft - 1, n, memo)

        if ytree is None:
            continue

        ntree = search(no, qleft - 1, n, memo)

        if ntree is None:
            continue

        tree = ("ask", asked, ytree, ntree)
        memo[key] = tree
        return tree

    memo[key] = None
    return None


def find_tree(n, q):
    return search(make_states(n), q, n, {})


def print_tree(tree, names, space=""):
    if tree[0] == "done":
        print(space + "Jewel is in " + names[tree[1]])
        return

    asked = tree[1]

    print(space + "Ask about " + names[asked])

    print(space + " YES:")
    print_tree(tree[2], names, space + "   ")

    print(space + " NO:")
    print_tree(tree[3], names, space + "   ")


def use_tree(tree, state):
    if tree[0] == "done":
        return tree[1]

    asked = tree[1]

    if answer(state, asked):
        return use_tree(tree[2], state)
    else:
        return use_tree(tree[3], state)


def state_name(state, names):
    vault, oracle = state

    if oracle:
        k = "Oracle"
    else:
        k = "Chimera"

    return "(" + names[vault] + ", " + k + ")"


# -------------------------------------------------
# Part (a)
# -------------------------------------------------

print("PART (a)")
print()

states = make_states(3)

for s in states:
    a = nested_answer(s, 0)

    if a:
        out = "YES"
    else:
        out = "NO"

    print(state_name(s, vaults), "->", out)

print()


# -------------------------------------------------
# Part (b)
# one yes/no answer cannot identify 3 vaults
# -------------------------------------------------

print("PART (b)")
print()

good = 0

# 6 hidden states, so 2^6 possible yes/no patterns
for mask in range(64):
    yes_vaults = set()
    no_vaults = set()

    for i in range(6):
        v = states[i][0]
        bit = (mask >> i) & 1

        if bit == 1:
            yes_vaults.add(v)
        else:
            no_vaults.add(v)

    if len(yes_vaults) <= 1 and len(no_vaults) <= 1:
        good += 1

print("Patterns checked:", 64)
print("Patterns that can identify the vault:", good)
print()


# -------------------------------------------------
# Part (c)
# -------------------------------------------------

print("PART (c)")
print()

pairs = set()

for v in range(3):
    # Oracle is enough here because nested question
    # gives the same result for Oracle and Chimera
    s = (v, True)

    a1 = nested_answer(s, 0)   # Coral
    a2 = nested_answer(s, 1)   # Amber

    p1 = "Y" if a1 else "N"
    p2 = "Y" if a2 else "N"

    pairs.add((p1, p2))

    print(vaults[v], "->", (p1, p2))

print()

if ("Y", "Y") not in pairs:
    print("(Y, Y) does not occur.")

print()


# -------------------------------------------------
# Part (d)
# -------------------------------------------------

print("PART (d)")
print()

for q in range(1, 4):
    tree = find_tree(3, q)

    if tree is None:
        print(q, "question(s): impossible")
    else:
        print(q, "question(s): possible")

print()

tree = find_tree(3, 3)

print("One tree found:")
print()
print_tree(tree, vaults)

print()

count = 0

for s in states:
    guess = use_tree(tree, s)

    if guess == s[0]:
        count += 1

    print(
        state_name(s, vaults),
        "->",
        vaults[guess]
    )

print()
print("Correct:", count, "out of", len(states))
print()


# -------------------------------------------------
# small experiment for more vaults
# -------------------------------------------------

print("GENERAL CHECK")
print()


def pattern(state, n):
    p = []

    for asked in range(n):
        p.append(answer(state, asked))

    return tuple(p)


def impossible_pair(n):
    st = make_states(n)

    for i in range(len(st)):
        for j in range(i + 1, len(st)):
            if st[i][0] == st[j][0]:
                continue

            if pattern(st[i], n) == pattern(st[j], n):
                return st[i], st[j]

    return None


for n in range(2, 8):
    pair = impossible_pair(n)

    if pair is not None:
        print("m =", n, "-> impossible")
        continue

    minimum = None

    for q in range(1, n + 1):
        if find_tree(n, q) is not None:
            minimum = q
            break

    if n == 3:
        expected = 3
    else:
        expected = n - 1

    print(
        "m =", n,
        "minimum =", minimum,
        "expected =", expected
    )
