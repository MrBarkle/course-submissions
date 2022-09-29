#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int get_length(long n);
long get_number(void);
long checksum(long n);
int sum_digits(int i);
void type(long n);

int main(void)
{

    // Prompt user for number
    long n = get_number();
    // Calculate checksum and print type if valid
    type(checksum(n));

}
/*
 * Function: get_number
 *
 * prompts user to input a credit card number
 * as long as that number is length of 13, 15, or 16
 *
 * Returns: the card number (of type long)
 *
 */
long get_number(void)
{
    long n;
    int length;
    
    // Ask for credit card number
    n = get_long("Number: ");
    length = get_length(n);
    
    // Make sure number is proper length
    if (length < 13 || length > 16 || length == 14)
    {
        // Print invalid then exit program
        printf("INVALID\n");
        exit(0);
    }
    else
    {
        // Return accepted input
        return n;
    }

}
/*
 * Function: get_length
 *
 * computes the length of a long type number
 * using the equation found at:
 * mathworld.wolfram.com/NumberLength.html
 *
 * n: the card number (of type long)
 *
 * Returns: the length of n 
 *
 */
int get_length(long n)
{
    // Compute length of n 
    int length = floor(log10(n)) + 1;
    // Return length
    return length;
}
/*
 * Function: checksum
 *
 * determines if the credit card number is
 * syntactically valid using steps from
 * Luhn’s algorithm
 *
 * n: the card number (of type long)
 *
 * Returns: n if checksum is 0 else exits
 *          after printing "INVALID"
 *
 */
long checksum(long n)
{
    long temp1 = n;
    long temp2 = n;
    int sum1 = 0;
    int sum2 = 0;
    int sum3;
    
    while (temp1 != 0)
    {   
        /* Look at the 2nd to last digit and 
        every other digit prior to that. Multiply 
        each by 2 and add the sum of their digits 
        to sum1. */
        sum1 += sum_digits(2 * ((temp1 % 100) / 10));
        temp1 /= 100;
        
    }
    while (temp2 != 0)
    {   
        // Find the sum of digits not used in sum1
        sum2 += (temp2 % 10);
        temp2 /= 100;
    }
    // Add all sums together
    sum3 = sum1 + sum2;
    // If syntactically valid continue
    if (sum3 % 10 == 0)
    {
        // Return n 
        return n;
    }
    // Otherwise return INVALID and exit
    else
    {
        printf("INVALID\n");
        exit(0);
    }
}
/*
 * Function: sum_digits
 *
 * computes the sum of all digits in 
 * a number
 *
 * i: a number of type int
 *
 * Returns: the sum of all digits in i
 *
 */
int sum_digits(int i)
{
    int temp = i;
    int sum = 0;
    // Loop through all digits and add to sum
    while (temp != 0)
    {
        sum += (temp % 10);
        temp /= 10;
    }
    // Return sum
    return sum;
}
/*
 * Function: type
 *
 * determines the type (if any) of 
 * the credit card number being checked
 *
 * n: the card number (of type long)
 *
 * Returns: the card type - VISA, 
 *          AMEX, MASTERCARD, or 
 *          INVALID
 *
 */
void type(long n)
{
    
    long temp = n;
    int length_n = get_length(n);
    int length_t = get_length(temp);
  
    // Get first 2 digits
    while (length_t > 2)
    {
        temp /= 10;
        length_t = get_length(temp);
    }
  
    // First digit of card number 
    int first = ((temp % 100) / 10);
    // Second digit of card
    int second = temp % 10;
  
    // Chance at being VISA
    if (length_n != 15 && (first == 4))
    {
        printf("VISA\n");
    }
    // Chance at being MASTERCARD
    else if (length_n == 16 && (first == 5))
    {
        if (second >= 1 && second <= 5)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // Chance at being AMEX
    else if (length_n == 15 && (first == 3))
    {
        if (second == 4 || second == 7)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}