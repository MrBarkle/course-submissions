from cs50 import get_string
from collections import Counter

# Capture text in Counter dict
text = Counter(get_string("Text: "))

# Find punctuation count
sentences = sum({v for c, v in text.items() if c in ".?!"})

# Find whitespace count
words = text[" "] + 1

# Find letters and total their count
letters = sum(({c: v for c, v in text.items() if c.isalpha()}).values())

# Calculate l and s for coleman-liau index equation
l = (letters/words)*100
s = (sentences/words)*100

# Calculate index
index = round((0.0588 * l) - (0.296 * s) - (15.8))

# Print results
if index >= 16:
    print("Grade 16+")
elif (index < 1):
    print("Before Grade 1")
else:
    print("Grade", index)