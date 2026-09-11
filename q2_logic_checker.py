from itertools import product

# True  = Oracle
# False = Chimera

chests = ["Jade", "Onyx", "Amber"]


def athena_statement(chest, athena):
    # "If the jewel is in the jade chest, then I am a chimera."
    jewel_in_jade = (chest == "Jade")
    athena_is_chimera = not athena

    # P -> Q is the same as (not P) or Q
    return (not jewel_in_jade) or athena_is_chimera


def boreas_statement(chest, cronus):
    # "Cronus is an oracle only if the jewel is in the onyx chest."
    cronus_is_oracle = cronus
    jewel_in_onyx = (chest == "Onyx")

    # "P only if Q" means P -> Q
    return (not cronus_is_oracle) or jewel_in_onyx


def cronus_statement(athena, demeter):
    # "At least one of Athena and Demeter is a chimera."
    athena_is_chimera = not athena
    demeter_is_chimera = not demeter

    return athena_is_chimera or demeter_is_chimera


def demeter_statement(boreas, cronus):
    # "Boreas and Cronus are of the same kind."
    return boreas == cronus


def statement_matches_speaker(speaker_is_oracle, statement_is_true):
    # Oracle -> statement must be true
    # Chimera -> statement must be false
    return speaker_is_oracle == statement_is_true


def check_world(chest, athena, boreas, cronus, demeter, use_clues=None):
    if use_clues is None:
        use_clues = {"Athena", "Boreas", "Cronus", "Demeter"}

    a_stmt = athena_statement(chest, athena)
    b_stmt = boreas_statement(chest, cronus)
    c_stmt = cronus_statement(athena, demeter)
    d_stmt = demeter_statement(boreas, cronus)

    if "Athena" in use_clues:
        if not statement_matches_speaker(athena, a_stmt):
            return False

    if "Boreas" in use_clues:
        if not statement_matches_speaker(boreas, b_stmt):
            return False

    if "Cronus" in use_clues:
        if not statement_matches_speaker(cronus, c_stmt):
            return False

    if "Demeter" in use_clues:
        if not statement_matches_speaker(demeter, d_stmt):
            return False

    return True


def kind_name(value):
    return "Oracle" if value else "Chimera"


def find_possible_worlds(use_clues=None):
    possible = []

    # 3 chest choices and 2^4 type choices = 48 total worlds
    for chest in chests:
        for athena, boreas, cronus, demeter in product([True, False], repeat=4):
            if check_world(
                chest,
                athena,
                boreas,
                cronus,
                demeter,
                use_clues
            ):
                possible.append(
                    (chest, athena, boreas, cronus, demeter)
                )

    return possible


def print_world(world):
    chest, athena, boreas, cronus, demeter = world

    print("Jewel:", chest)
    print("Athena :", kind_name(athena))
    print("Boreas :", kind_name(boreas))
    print("Cronus :", kind_name(cronus))
    print("Demeter:", kind_name(demeter))


# ------------------------------------------------------------
# Part 1: check the full puzzle
# ------------------------------------------------------------

all_clues = {"Athena", "Boreas", "Cronus", "Demeter"}
solutions = find_possible_worlds(all_clues)

print("Total possible worlds checked: 48")
print("Worlds satisfying all four speeches:", len(solutions))
print()

for world in solutions:
    print_world(world)
    print()


# ------------------------------------------------------------
# Part 2: check whether every speech is actually necessary
# ------------------------------------------------------------

print("-" * 45)
print("Removing one speech at a time")
print("-" * 45)

for removed in ["Athena", "Boreas", "Cronus", "Demeter"]:
    remaining = all_clues - {removed}
    worlds = find_possible_worlds(remaining)

    print()
    print("Speech removed:", removed)
    print("Number of possible worlds:", len(worlds))

    # Print only a few examples so the output does not become too long
    for world in worlds[:5]:
        chest, athena, boreas, cronus, demeter = world
        print(
            " ",
            chest,
            "|",
            kind_name(athena),
            kind_name(boreas),
            kind_name(cronus),
            kind_name(demeter)
        )
