import math
import nltk
import os
import string
import sys

from collections import Counter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    # Get directory path
    path = os.path.join(os.getcwd(), directory)

    # Create empty dictionary
    contents = {}

    # For each file in directory
    for file in os.listdir(path):
        # Open file (key) and read its contents (value)
        with open(os.path.join(path, file), encoding='utf-8') as f:
            # Set key value pairs in dictionary
            contents[file] = f.read()

    # Return dictionary
    return contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    filtered = []

    # If issues using stopwards, uncomment next line.
    # nltk.download('stopwords')

    # Filter tokenized document based on the condition that each word is not
    # found in string.punctuation, nltk.corpus.stopwords.words("english") and
    # contains at least one alphabetic character
    filtered.extend([word for word in nltk.word_tokenize(document.lower())
                    if any(c.isalpha() for c in word) and word not in
                    string.punctuation and word not in
                    nltk.corpus.stopwords.words("english")])

    # Return filtered document
    return filtered


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Recall that the inverse document frequency of a word is defined by taking
    the natural logarithm of the number of documents divided by the number of
    documents in which the word appears.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # Get the numbre of documents
    num_documents = len(documents)

    # Get a list of all words in all documents
    words = set([word for word_list in documents.values() for word in word_list])

    idfs = {}

    # Look at each unique word in the corpus
    for word in words:
        count = 0
        # For each document
        for document in documents.values():
            # If the word is in the document
            if word in document:
                # Increase count
                count += 1

        # Calculate inverse document frequency for 'word'
        idf = math.log(num_documents / count)

        # Add to dictionary
        idfs[word] = idf

    # Return dictionary of words to IDF values
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.

    Recall that tf-idf for a term is computed by multiplying the number of times
    the term appears in the document by the IDF value for that term.

    Files should be ranked according to the sum of tf-idf values for any word in
    the query that also appears in the file
    """

    # Initialize dict of TF-IDF values totals for each file in files
    tf_idfs = {file: 0 for (file, value) in files.items()}

    # Loop over each unique word in the query set
    for word in query:
        # Loop over each file and its list of words
        for file, file_words in files.items():
            # Get the count of each word occurance in file's word list
            c = Counter(file_words)
            # Check if word is in the document
            if word in c:
                # Get the number of times the word appears in the document
                appears = c[word]
                # Calculate TF-IDF for the word
                tf_idf = appears * idfs[word]
                # Add TF-IDF value to sum of file's TF-IDF values
                tf_idfs[file] += tf_idf

    # Sort files according to descending TD-IDF values
    ranked = dict(sorted(tf_idfs.items(), key=lambda item: item[1], reverse=True))

    # Get top 'n' number of files
    top = list(ranked.keys())[0: n]

    # Return list top files
    return top


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # Initialize dict of total IDF values for each sentence in sentences
    total_idfs = {sentence: [0, 0] for (sentence, value) in sentences.items()}

    # Loop over each unique word in the query
    for word in query:
        # Loop over each sentence
        for sentence in sentences:
            # Get the count of each word occurance in sentence
            c = Counter(sentences[sentence])
            # Get sentence length (number of words)
            len_sentence = len(sentences[sentence])
            # If the word is in the sentence
            if word in sentences[sentence]:
                # Update IDF value based on word frequency
                total_idfs[sentence][0] += idfs[word]

            # Update the query term density for each sentence
            total_idfs[sentence][1] += (c[word] / len_sentence)

    # Sort files according to total IDF values then Query Term Density second
    ranked = dict(sorted(total_idfs.items(), key=lambda item:
                         (item[1][0], item[1][1]), reverse=True))

    # Get top 'n' number of files
    top = list(ranked.keys())[0: n]

    # Return list top files
    return top


if __name__ == "__main__":
    main()
