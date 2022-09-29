import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    evidence = []
    labels = []

    # Open CSV file
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for user in reader:
            # Create next user list inside evidence
            evidence.append([
                int(user['Administrative']),
                float(user['Administrative_Duration']),
                int(user['Informational']),
                float(user['Informational_Duration']),
                int(user['ProductRelated']),
                float(user['ProductRelated_Duration']),
                float(user['BounceRates']),
                float(user['ExitRates']),
                float(user['PageValues']),
                float(user['SpecialDay']),
                months(user['Month']),
                int(user['OperatingSystems']),
                int(user['Browser']),
                int(user['Region']),
                int(user['TrafficType']),
                int(user['VisitorType'] == 'Returning_Visitor'),
                int(user['Weekend'] == 'TRUE')
            ])
            # Label (Revenue)
            labels.append(int(user['Revenue'] == 'TRUE'))

    # Return tuple of evidence and labels
    return (evidence, labels)


def months(month):
    """
    Takes a month string and converts it to an INT type

    NOTE: The months of January and April were not found in the user data within
    the .csv file therefore Its assumed that their abrreviations are Jan and Apr

    """
    return {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11,
    }[month]


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # Specify the model type
    model = KNeighborsClassifier(n_neighbors=1)

    # Fit model
    model.fit(evidence, labels)

    # Return model
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # Total identified negatives
    ident_negatives = 0.0
    # Total negative examples
    negative = 0.0

    # Total identified positives
    ident_positives = 0.0
    # Total positive examples
    positive = 0.0

    # Loop through labels and corresponding predictions
    for label, prediction in zip(labels, predictions):

        # Check negatives
        if label == 0:
            negative += 1.0
            if label == prediction:
                ident_negatives += 1.0

        # Check positives
        if label == 1:
            positive += 1.0
            if label == prediction:
                ident_positives += 1.0

    # Calculate and return True Positive Rate and True Negative Rate
    return ident_positives / positive, ident_negatives / negative


if __name__ == "__main__":
    main()
