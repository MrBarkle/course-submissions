import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # Define a joint probability
    joint_prob = 1

    # For each person in people
    for person in people:

        # Determine the person's gene count and trait status
        genes = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False

        # Next determine if the person has parent data listed
        mother, father = people[person]["mother"], people[person]["father"]

        # If no parents are listed
        if not mother and not father:
            # Use the standard probability distribution
            joint_prob *= PROBS["gene"][genes]

        # We can assume if one parent is listed then both are listed
        # Each parent will pass one of their two genes on to their child
        # randomly plus there is a chance it mutates
        else:
            # Find probability associated with number of genes from the mother
            if mother in two_genes:
                # Mother's probability given that she has two gene copies
                mother_prob = 1 - PROBS["mutation"]
            elif mother in one_gene:
                # Mother's probability given that she has one gene copy
                mother_prob = 0.5
            else:
                # Mother's probability given that she has no gene copies
                mother_prob = PROBS["mutation"]

            # Do the same for the father
            if father in two_genes:
                # Father's probability given that he has two gene copies
                father_prob = 1 - PROBS["mutation"]
            elif father in one_gene:
                # Father's probability given that he has one gene copy
                father_prob = 0.5
            else:
                # Father's probability given that he has no gene copies
                father_prob = PROBS["mutation"]

            # Based on gene count and parent data determine person's probability
            if genes == 0:
                # Person's probability of having 0 genes
                joint_prob *= (1 - mother_prob) * (1 - father_prob)
            elif genes == 1:
                # Person's probability of having 1 gene
                joint_prob *= mother_prob * (1 - father_prob) + (1 - mother_prob) * father_prob
            else:
                # Person's probability of having 2 genes
                joint_prob *= mother_prob * father_prob

        # Compute the probability that a person does or does not have a trait
        joint_prob *= PROBS['trait'][genes][trait]

    # Return the full joint probability
    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # For each person update probability with new joint probability
    for person in probabilities:
        # Determine the person's gene count and trait status
        genes = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False

        # Update probabilities dictionary
        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # For each person
    for person in probabilities:
        # Calculate 1 / total probabilities for 'gene' and 'trait' each
        gene_multiplier = (1 / sum(probabilities[person]["gene"].values()))
        trait_multiplier = (1 / sum(probabilities[person]["trait"].values()))

        # Normalize distributions for genes so probabilities sum to 1
        for g, p in probabilities[person]['gene'].items():
            probabilities[person]['gene'][g] = (p * gene_multiplier)

        # Normalize distributions for traits so probabilities sum to 1 
        for t, p in probabilities[person]['trait'].items():
            probabilities[person]['trait'][t] = (p * trait_multiplier)


if __name__ == "__main__":
    main()
