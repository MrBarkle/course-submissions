#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int validate(int c, string k);
void encipher(string k, string p);

int main(int argc, string argv[])
{
    // Validate user input
    if (validate(argc, argv[1]) == 1)
    {
        // Return 1 if there is an error
        return 1;
    }
    // Prompt user for plaintext to encipher
    string plaintext = get_string("plaintext:  ");
    // Encipher plain text
    encipher(argv[1], plaintext);
    // Return 0 after successful run
    return 0;
}
/*
 * Function: validate
 *
 * Validates the users input by checking if
 * it is 26 characters long and consisting of
 * non duplicate alphabetic characters only. 
 *
 * int c: the number of arguments passed in
 *        including the name of the program
 *
 * string k: argv[1] aka the key string 
 *           passed in by the user at run time
 *
 * Return: 0 if valid, 1 if invalid
 *
 */
int validate(int c, string k)
{
    if (c != 2)
    {
        // Make sure user includes a key when run
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if (strlen(k) > 26)
    {
        // Make sure the key is 26 characters long 
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    for (int i = 0; i < 26 - 1; i ++) 
    {
        for (int j = i + 1; j < 26; j ++) 
        {
            if (isalpha(k[i]) == 0)
            {
                // Make sure the key only contains alphabetic characters 
                printf("Key must only contain alphabetic characters.\n");
                return 1;
            }
            if (k[i] == k[j]) 
            { 
                // Make sure the key doesnt repeat characters
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
            if (tolower(k[i]) == tolower(k[j]))
            {
                // Make sure the key doesnt repeat characters (case sensitive)
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }
    // Return 0 if valide 
    return 0;
}
/*
 * Function: encipher
 *
 * Encipher p using k
 *
 * string k: argv[1] aka the key string 
 *           passed in by the user at run time
 * 
 * string p: user input string to encipher
 *
 */
void encipher(string k, string p)
{
    // Poor programming fix to previous error, convert key to all lowercase
    for (int j = 0; j < 26; j ++)
    {
        if (isupper(k[j]))
        {
            k[j] = tolower(k[j]);
        }
    }// This handles mis-match-case keys but adds time complexity
    
    // Get length of plaintext
    int len = strlen(p);
    printf("ciphertext: ");
    // Loop each character of plaintext
    for (int i = 0; i < len; i ++)
    {
        // If the character is alphabetic and uppercase
        if (isalpha(p[i]) && isupper(p[i]))
        {
            // Print corresponding cipher character
            printf("%c", toupper(k[p[i] - 'A']));
        }
        // If the character is alphabetic and lowercase
        else if (isalpha(p[i]) && islower(p[i]))
        {
            // Print corresponding cipher character
            printf("%c", tolower(k[p[i] - 'a']));
        }
        // If non alphabetic
        else
        {
            // Print non alphabetic character as is
            printf("%c", p[i]);
        }
    }
    // Print new line to finish output
    printf("\n");
}