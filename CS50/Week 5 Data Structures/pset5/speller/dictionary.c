// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include "dictionary.h"
#include <ctype.h>

#define MULTIPLIER (37)

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26 * 26;

// Hash table
node *table[N];

// Keep track of words
int WORD_COUNT = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //Hash word to obtain hash value
    int h = hash(word);

    // Search for word at index provided by hash function
    for (node *tmp = table[h]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(tmp -> word, word) == 0)
        {
            // If word in dictionary
            return true;
        }
    }
    // Else if word not in dictionary
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    /* From Kernighan and Ritchie's "The C Programming Language"
       and Yale's 4.2 Multiplication Method Notes

       https://www.strchr.com/hash_functions

       https://www.cs.yale.edu/homes/aspnes/pinewiki/
       C(2f)HashTables.html?highlight=%28CategoryAlgorithmNotes%29
       
       Plus tried to make this account for case insensitivity

       */

    int h = 0;

    while (*word)
    {
        h  = MULTIPLIER * h + tolower(*word++);
    }

    // Return h % N so the value stays within the scope of the array
    return h % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open file.\n");
        // Return 1 if unsuccessful
        return false;
    }
    
    // Create buffer location for words to be placed
    char buffer[LENGTH + 1];

    // Read string from file one at a time, store in buffer temporarily
    while (fscanf(file, "%s", buffer) == 1)
    {
        // Allocate memory for new node
        node *n = malloc(sizeof(node));

        // If we have memory, create node
        if (n != NULL)
        {
            // Copy word into node
            strcpy(n -> word, buffer);
            // Set pointer to next
            n -> next = NULL;
        }

        // Hash word to get index
        int h = hash(n -> word);

        // Insert node at front of list
        n -> next = table[h];
        table[h] = n;

        WORD_COUNT ++;
    }

    // Close file
    fclose(file);

    // Return 0 if successful
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return number of words in dictionary, if any.
    return WORD_COUNT;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // For each index of the array of linked lists
    for (int i = 0; i < N; i ++)
    {
        // While the linked list at index i hasnt fully been freed
        while (table[i] != NULL)
        {
            // Point to next node first
            node *tmp = table[i] -> next;
            // Free first node
            free(table[i]);
            // Set the start of the list to point to the next node
            table[i] = tmp;
        }
    }
    // Return true once the dictionary is unloaded
    return true;
}
