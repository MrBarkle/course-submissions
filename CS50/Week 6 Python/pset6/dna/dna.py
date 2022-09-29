from sys import argv
import pandas as pd
import re

# Only accept valid run sequence
if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

# Read in csv file
df = pd.read_csv(argv[1], index_col=0)

# Open text file
with open(argv[2], 'r') as text:
    seq = text.read()

find = []
# Loop through each pattern
for rep in df.columns:
    '''Use regex to find the largest consecutive sequence of a given pattern
    Find continuous occurances of 'rep' in seq
    Look for the maximum length of all subsequences
    Take longest subsequence and divide it by the length of 'rep' to get
    the number of times that 'rep' repeated in that subsequence'''
    try:
        longest = len(max(re.findall(r'(?:'+rep+')+', seq), key=len))//len(rep)
    # If 'rep' not in seq then use 0
    except:
        longest = 0
    find.append(longest)

# This took me too long to figure out how to extract name!
name = df[(df.isin(find)).all(True)].index.tolist()
# Print the name if it exists
if len(name) == 0:
    print("No match")
else:
    print(*name)