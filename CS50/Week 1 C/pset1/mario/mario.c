#include <stdio.h>
#include <cs50.h>

int get_height(void);
void build_pyramid(int h);

int main(void)
{
    // First prompt the user for a height bewteen 1 and 8
    int i = get_height();
    // Construct the pyramid from input height
    build_pyramid(i);
}

int get_height(void)
{
    int n;
    
    do
    {
        // Prompt user for height 
        n = get_int("Height: ");
    }
    // Keep asking if not within these constraints
    while (n < 1 || n > 8);
    
    return n;
}

void build_pyramid(int h)
{
    
    // Use this for #'s to print
    int n = 1;
    
    // Print new line until pyramid height reached
    while (n < h + 1)
    {
        // Print spaces on left
        printf("%.*s", (h - n), "        ");
        // Print #'s on left
        printf("%.*s", (n), "########");
        // Print gap
        printf("  ");
        // Print right side #
        printf("%.*s\n", (n), "########");
        // Increase n by 1 for next layer
        n ++;
        
        /* This method works since we know the
        upper bounds of # that can be printed */
        
    }
}