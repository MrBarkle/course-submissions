import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP | S Conj S | S P S
NP -> N | N NP | Adj NP | Adv NP | Conj NP | P NP | N Adv | N P Det NP
VP -> V | V NP | Adv VP | V Adv | V Det NP | Det N VP | V P Det NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Uncomment the below line if experiencing issues with word_tokenize call
    # on the first run of this application!

    # nltk.download('punkt')

    filtered = []

    # Add lowercase strings containing at least one alphabetic char to list
    filtered.extend([word.lower() for word in nltk.word_tokenize(sentence)
                    if any(c.isalpha() for c in word)])

    # Return list of words
    return filtered


def check(tree):
    """
    Returns True if the tree contains an NP label, otherwise False
    """

    # Loop through subtrees
    for subtree in list(tree):
        # Check is subtree has NP label
        if subtree.label() == 'NP':
            # If yes, return True
            return True
        # If not NP label
        else:
            # Check if subtree has multiple children
            if len(subtree) != 1:
                if check(subtree) == True:
                    return True
    return False


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    chunks = []

    # Find all subtrees of tree that start with NP label
    for subtree in tree.subtrees(lambda x: x.label() == 'NP'):

        # If the subtree doesn't have children
        if len(subtree) == 1:

            # Add to NP chunks, no need to check
            chunks.append(subtree)

        # Check subtree for NP within itself
        elif check(subtree) != True:

            # Store proper NP chunks
            chunks.append(subtree)

    # Return list of NP chunks
    return chunks


if __name__ == "__main__":
    main()
