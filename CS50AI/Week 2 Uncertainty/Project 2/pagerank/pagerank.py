import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Initialize empty dict of corpus pages
    result = dict.fromkeys(corpus.keys(), 0.0)

    # If page has no links
    if len(corpus[page]) == 0:
        # Set all page probablities to equal value
        for key in corpus:
            # If a page has no links, we can pretend it has links to all pages
            # in the corpus, including itself
            result[key] += 1 / len(corpus)

        # Return probability distribution
        return result

    # In the case that the page does have links
    for key in corpus:
        # If input page links to key page
        if key in corpus[page]:
            # Set probability of following page link
            result[key] += damping_factor / len(corpus[page])
        # Set probability of following page at random
        result[key] += (1 - damping_factor) / len(corpus)

    # Return probability distribution
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize empty dict of corpus pages with probabilites set to 0
    pages = dict.fromkeys(corpus.keys(), 0.0)

    # Choose pseudorandom starting page
    start = random.choice(list(corpus))

    # Set probability of random page
    pages[start] += (1 / n)

    # The next sample should be generated from the prev sample
    prev = start

    # For the remaining samples, use transition_model to pick pages
    for sample in range(0, n - 1):
        # Get probability distribution of previous sample using transition model
        prob_dist = transition_model(corpus, prev, damping_factor)
        # Use prob_dist of prev to get page for next sample
        prev = random.choices(list(prob_dist.keys()),
                              weights=list(prob_dist.values()))[0]
        # Increment visit for this page
        pages[prev] += (1 / n)

    # Return estimated PageRank for each page
    return pages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Total number of pages in the corpus (at least 1)
    n = len(corpus)

    # Assign each page a rank of 1/n in a new dict initially
    cur_prs = dict.fromkeys(corpus.keys(), (1 / n))

    # Initialize dict to keep track of updated PageRanks
    new_prs = dict.fromkeys(corpus.keys(), None)

    # Constant condition in which surfer chose page at random
    random_prob = (1 - damping_factor) / n

    # Difference between current PageRank values and new PageRank values
    max_diff = (1 / n)

    # Repeat until no PageRank value changes by more than 0.001 threshold
    while max_diff > 0.001:

        # Reset the PageRank difference each iteration
        max_diff = 0

        # For all pages in the corpus
        for p in corpus:
            # Condition in which the surfer chose a link from page i to p
            link_prob = sum([(1 / n) * cur_prs[i] if len(corpus[i]) == 0
                            else cur_prs[i] / len(corpus[i]) if p in corpus[i]
                            else 0 for i in corpus])

            # Set new PageRank for p using full formula from background
            new_prs[p] = random_prob + (damping_factor * link_prob)

        # Assure the sum of the PageRank values is 1 by adjusting all values
        new_prs = {key: (value / sum(new_prs.values()))
                   for key, value in new_prs.items()}

        # Find the largest difference in PageRank
        for p in corpus:
            # Get difference between current PageRank and new PageRank
            cur_diff = cur_prs[p] - new_prs[p]
            # If a new maximum difference in ranks is found
            if abs(cur_diff) > max_diff:
                # Set varaible
                max_diff = cur_diff

        # Update current rankings with new rankings
        cur_prs = new_prs.copy()

    # Return dictionary of PageRanks
    return cur_prs


if __name__ == "__main__":
    main()
