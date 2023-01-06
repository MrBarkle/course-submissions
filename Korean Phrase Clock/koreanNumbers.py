class KoreanNumber():
    '''
    A Class to represent an integer as Korean characters meant to be pronounced
    This class converts a number in the form of an integer and returns a string
    representation of that number in Sino Korean

    :author:    Brandon Barkle <linkedin.com/in/brandonbarkle>
    :date:      1/5/2023
    '''

    def __init__(self, number):
        self.number = number

    def _convert_to_sino(self):
        '''
        Takes the integer value stored at self.number and converts it to the 
        pronounced form of that number in Korean. For example, 1992 would be 
        converted to and spoken as 천구백구십이. 

        :returns:    an integer converted to a number written in Sino Korean
        :rtype:      string

        '''
        # Get length of number
        n = len("%i" % self.number)

        # Sino Korean numbers
        sino = {0: '영', 1: '일', 2: '이', 3: '삼', 4: '사', 5: '오', 6: '육',
                7: '칠', 8: '팔', 9: '구', 10: '십', 100: '백', 1000: '천', }

        def _get_units_place(num):
            '''
            Takes an int and converts it to the pronounced form of that int
            in Korean. For example 8 would be converted to 팔.

            :param num:     a number representing the 1's position to 
                            convert to Korean; that is 0 - 9
            :type num:      int

            :returns:       an integer converted to written Sino Korean
            :rtype:         string
            '''
            return sino[num]

        def _get_tens_place(num):
            '''
            Takes an int and converts it to the pronounced form of that int
            in Korean. For example 11 would be converted to 십일.

            :param num:     a number representing the 10's position to convert
                            to Korean; that is 10 - 99
            :type num:      int

            :returns:       an integer converted to written Sino Korean
            :rtype:         string
            '''
            # Base case
            if num == 10:
                return sino[10]

            # 10's place digit
            tens = num // 10

            # If not a number divisible by 10
            if num % 10 != 0:

                # Get units place
                units = sino[num % 10]

                # Get tens place in Korean next
                if tens == 1:
                    # 11 - 19
                    tens = sino[10]
                else:
                    # 21- 29, 31-39, ..., 91-99
                    tens = f"{sino[tens]}{sino[10]}"

                # Return whole number
                return f"{tens}{units}"

            # 20, 30, ..., 90
            else:
                return f"{sino[tens]}{sino[10]}"

        def _get_hundreds_place(num):
            '''
            Takes an int and converts it to the pronounced form of that int
            in Korean. For example 123 would be converted to 백이십삼.

            :param num:     a number representing the 100's position to convert
                            to Korean; that is 100 - 999
            :type num:      int

            :returns:       an integer converted to written Sino Korean
            :rtype:         string
            '''
            # Base case
            if num == 100:
                return sino[100]

            # 100's place digit
            hundreds = (num % 1000) // 100

            # Get remainder
            tens = num % 100

            # If not a number divisible by 100
            if num % 100 != 0:

                # If leading zero on remainder (found by checking the length)
                match len("%i" % tens):
                    case 1:
                        remainder = _get_units_place(tens)
                    case _:
                        remainder = _get_tens_place(tens)

                # Get hundreds place in Korean
                if hundreds == 1:
                    return f"{sino[100]}{remainder}"

                else:
                    return f"{sino[hundreds]}{sino[100]}{remainder}"

            # 200, 300, ..., 900
            else:
                return f"{sino[hundreds]}{sino[100]}"

        def _get_thousands_place(num):
            '''
            Takes an int and converts it to the pronounced form of that int
            in Korean. For example 9000 would be converted to 구천.

            :param num:     a number representing the 1000's position to convert
                            to Korean; that is 1000 - 9999
            :type num:      int

            :returns:       an integer converted to written Sino Korean
            :rtype:         string
            '''
            # Base case
            if num == 1000:
                return sino[1000]

            # 1000's place digit
            thousands = num // 1000

            # Get remainder
            hundreds = num % 1000

            # If not a number divisible by 1000
            if num % 1000 != 0:

                # If leading zero on remainder (found by checking the length)
                match len("%i" % hundreds):
                    case 1:
                        remainder = _get_units_place(hundreds)
                    case 2:
                        remainder = _get_tens_place(hundreds)
                    case _:
                        remainder = _get_hundreds_place(hundreds)

                # Get thousands place in Korean
                if thousands == 1:

                    return f"{sino[1000]}{remainder}"

                else:
                    return f"{sino[thousands]}{sino[1000]}{remainder}"

            # 200, 300, ..., 900
            else:
                return f"{sino[thousands]}{sino[1000]}"

        # Must be using Python v3.10 or later to use match:case
        match n:
            # 1 - 9
            case 1:
                return _get_units_place(self.number)
            # 10 - 99
            case 2:
                return _get_tens_place(self.number)
            # 100 - 999
            case 3:
                return _get_hundreds_place(self.number)
            # 1000 - 9999
            case 4:
                return _get_thousands_place(self.number)
            case _:
                return "An error has occurred. Make sure value is between 0-9999"

    def __str__(self) -> str:
        '''
        Allows the number stored in self.number to be converted from an int and
        printed out as a string.

        :returns:    an integer converted to a number written in Sino Korean
        :rtype:     string
        '''
        return self._convert_to_sino()


def main():
    '''
    Convert a number directly from the command-line to Sino Korean

    :usage:             python koreanNumbers.py number
    :param number:      a user input number between 0 and 9999
    :type number:       string
    '''
    import sys  # Only need this import if calling from command-line

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python koreanNumbers.py number")

    number = sys.argv[1]

    # Make sure user inputs a valid positive number between 0 and 9999
    if number.isdigit() and int(number) >= 0 and int(number) <= 9999:
        print(KoreanNumber(int(number)))
    else:
        sys.exit(
            "Enter a valid number between 0 and 9999.\nUsage: python koreanNumbers.py number")


if __name__ == '__main__':
    main()

'''
Cited Sources

Line's containing: len("%i" % i) taken from suggestion in this thread:
https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer

Singling out specific digits described here
https://stackoverflow.com/questions/32752750/how-to-find-the-numbers-in-the-thousands-hundreds-tens-and-ones-place-in-pyth

'''
