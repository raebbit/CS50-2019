#include <cs50.h>
#include <stdio.h>
#include <math.h>

float get_non_negative(string prompt);

int main(void)
{
    float d = get_non_negative("Change owed: ");
    int c = round(d * 100);
    printf("%i\n\n", c);
    
    //get the each coins
    int q = c / 25;
    int remainder_1 = c % 25;
    int m = remainder_1 / 10;
    int remainder_2 = remainder_1 % 10;
    int n = remainder_2 / 5;
    int p = remainder_2 % 5;
    
    printf("Quarter: %i\n", q);
    printf("Dime: %i\n", m);
    printf("Nickel: %i\n", n);
    printf("Penny: %i\n", p);
    
    printf("Total number of coins: %i\n", q + m + n + p);
} 

// prompt user for non-negative number
float get_non_negative(string prompt)
{
    float f;
    do 
    {
        f = get_float("%s", prompt);
    }
    while (f < 0);
    return f;
}
