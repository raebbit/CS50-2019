#include <cs50.h>
#include <stdio.h>

int get_height(string prompt);

//get the height from 1 to 8
int get_height(string prompt)
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n < 1 || n > 8);
    return n;
}

int main(void)
{
    int n = get_height("Height: ");
    
    //build the wall!
    for (int i = 0; i < n; i++)
    {
        for (int k = n - 2; k >= i; k--)
        {
            printf(" ");
        }
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("  ");
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
