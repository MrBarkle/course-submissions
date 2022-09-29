#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // prompt the user for a name
    string name = get_string("What's your name?\n");
    // print 'hello' followed by the users answer to name
    printf("hello, %s\n", name);
}