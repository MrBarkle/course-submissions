#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

void find_index(string s);

// Define global variables
int LETTERS = 0;
int WORDS = 1;
int SENTENCES = 0;

int main(void)
{
    // Prompt user for text
    string text = get_string("Text: ");
    // Calculate grade
    find_index(text);
}
/*
 * Function: find_index
 *
 * Determines the reading level grade of 
 * string t using the coleman-liau index
 * defined as: Index = 
 * (0.0588 * L) - (0.296 * S) - (15.8)
 *
 * Makes use of global variables LETTERS,
 * WORDS, and SENTENCES to avoid looping 
 * through the text 3 times.
 *
 * string t: text passed in by user
 *
 */
void find_index(string t)
{
    // Get the length of t
    int len = strlen(t);
    // Loop through each letter of t
    for (int i = 0; i < len; i++)
    {
        // Count alphabetic characters
        if (isalpha(t[i]) > 0)
        {
            LETTERS ++;
        }
        // Count white space characters to infer word count
        if (isspace(t[i]) > 0)
        {
            WORDS ++;
        }
        // Count punctuation to infer number of sentences
        if (t[i] == '.' || t[i] == '!' || t[i] == '?')
        {
            SENTENCES ++;
        }
        
    }
    // Calculate l and s in coleman-liau index equation 
    float l = (float)LETTERS / (float)WORDS * 100;
    float s = (float)SENTENCES / (float)WORDS * 100;
    
    // Calculate index
    int index = round((0.0588 * l) - (0.296 * s) - (15.8));
    
    // Print Grade
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
