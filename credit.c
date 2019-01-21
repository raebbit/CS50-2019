#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    long long c = get_long_long("Number: ");
    
    //get sum using Luhn's algorithm
    int sum_2 = 0;
    for (int n = 2; n < 17; n += 2)
    {
        long long x = pow(10, n);
        long long y = pow(10, n - 1);
        int d = (c % x) / y;
        int d_2 = d * 2;
        if (d_2 > 9)
        {
            int a = d_2 % 10;
            int b = (d_2 % 100) / 10;
            d_2 = a + b;
        }
        
        sum_2 = sum_2 + d_2;
    }
      
    int sum_1 = 0;
    for (int n = 1; n < 17; n += 2)
    {
        long long x = pow(10, n);
        long long y = pow(10, n - 1);
        int d = (c % x) / y;
         
        sum_1 = sum_1 + d;
    }
    int sum = sum_2 + sum_1;
    int l = sum % 10 ;
     
    if (l == 0)
    {
        //valid card by company
        int i = c / pow(10, 13);
    
        if (((pow(10, 14) <= c) && (c < pow(10, 15))) && (i == 34 || i == 37))
        {
            printf("AMEX\n");
        }
        
        int j = c / pow(10, 14);
        if (((pow(10, 15) <= c) && (c < pow(10, 16))) && (j == 22 || (51 <= j && j <= 55)))
        {
            printf("MASTERCARD\n");
        }
     
        int k = c / pow(10, 12); 
        int m = c / pow(10, 15) ;
        if ((((pow(10, 12) <= c) && (c < pow(10, 13))) && k == 4) || (((pow(10, 15) <= c) && (c < pow(10, 16))) && m == 4))
        {
            printf("VISA\n");
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
