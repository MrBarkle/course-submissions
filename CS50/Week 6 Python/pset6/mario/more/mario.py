from cs50 import get_int

height = -1
# Prompt the user for a height between 1 and 8
while height < 1 or height > 8:
    height = get_int("Height: ")

n = 1
# Print a pyramid of that height
while n < height + 1:
    print(((height - n) * " ") + (n * "#") + "  " + (n * "#"))
    n += 1