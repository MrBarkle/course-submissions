from cs50 import get_string


# Copy of my C code for single digit sums
def sum_d(i):
    temp = i
    s = 0
    while temp != 0:
        s += temp % 10
        temp //= 10
    return s
    
    
# Prompt user for card number, store as list of ints
number = list(map(int, get_string("Number: ")))
# Store number's length
length = len(number)

# Make sure number is proper length
if length < 13 or length > 16 or length == 14:
    print("INVALID")
# If valid
else:
    # Compute second-to-last digit sums 
    sum1 = sum([sum_d(i * 2) for i in number[-2::-2]])
    # Compute remaining sums
    sum2 = sum([i for i in number[::-2]])
    
    # If syntactically valid (contains 0 at end)
    if ((sum1 + sum2) % 10) == 0:
        # VISA check
        if length != 15 and number[0] == 4:
            print("VISA")
        # MASTERCARD check
        elif length == 16 and number[0] == 5:
            print("MASTERCARD" if number[1] >= 1 and number[1] <= 5 else "INVALID")
        # AMEX check
        elif length == 15 and number[0] == 3:
            print("AMEX" if number[1] == 4 or number[1] == 7 else "INVALID")
        # INVALID
        else:
            print("INVALID")
    else:
        print("INVALID")