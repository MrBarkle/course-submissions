from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    # One of these has to be true
    Or(AKnight, AKnave),
    # If A is a Knight (telling truth) then A is both a Knight and a Knave
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # One of these has to be true
    Or(AKnight, AKnave),
    # One of these has to be true
    Or(BKnight, BKnave),
    # If A is a Knight (telling truth) then both must be Knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a Knave (not telling truth) then the opposite of its statement is
    # true which means B is Not a Knave
    Implication(AKnave, Not(BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # One of these has to be true
    Or(AKnight, AKnave),
    # One of these has to be true
    Or(BKnight, BKnave),
    # If A is a Knight (telling truth) then A and B are Knights
    Implication(AKnight, And(AKnight, BKnight)),
    # If B is a Knight (telling truth) then A is a Knave
    Implication(BKnight, And(AKnave, BKnight)),
    # If B is a Knave (not telling truth) then A is a Knight
    Implication(BKnave, And(AKnight, BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # One of these has to be true
    Or(AKnight, AKnave),
    # One of these has to be true
    Or(BKnight, BKnave),
    # One of these has to be true
    Or(CKnight, CKnave),
    # If A is a Knight (telling truth) then A is a Knight
    Implication(AKnight, AKnight),

    # If A says it's a Knave (not telling truth) then A is a not a Knave but has
    # to be a Knight, a Knight would never be able to say it was a Knave
    #Implication(AKnave, Not(AKnave)),

    # If B is a Knight (telling truth) then A said 'I am a Knave' which is a lie
    # and B also said C is a knave
    Implication(BKnight, And(Not(AKnave), CKnave)),
    # If B is a Knave (not telling truth) then A didn't say it was a Knave,
    # which makes it a Knight, and B said C is a knave, which makes it a Knight
    Implication(BKnave, And(AKnight, CKnight)),

    # If C is a Knight (telling truth) then A is a Knight
    Implication(CKnight, AKnight),
    # If C is a Knave (not telling truth) then A is a Knave
    Implication(CKnave, AKnave)

    # Seems to be other ways to do this
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
