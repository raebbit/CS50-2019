#include <cs50.h>
#include <stdio.h>

int get_height(string prompt);

// prompt user for the number between 1 and 8
int get_height(string prompt)
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n > 8 || n < 1);
    return n;
}

int main(void)
{
    int i = get_height("Height: ");
    
    //build tha wall!
    for (int j = 0; j < i; j++)
    {
        int l, k;
        for (l = i - 2; l >= j; l--)
        {
            printf(" ");
        }
        for (k = 0; k <= j; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}




