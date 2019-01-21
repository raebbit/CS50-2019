#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int shift(char c);

int main(int argc, string argv[])
{
    //get keyword correctly
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    else
    {
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            int a = argv[1][i];
            if (isalpha(a) == 0)
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
       
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        
        for (int i = 0, j = 0, n = strlen(plaintext); i < n; i++, j++)
        {
            int p = (int) plaintext[i];
            int key = shift(argv[1][j % strlen(argv[1])]);
            
            if (isupper(p))
            {
                int c;
                c = 65 + ((p - 65) + key) % 26;
                printf("%c", c);
            }
            else if (islower(p))
            {
                int c;
                c = 97 + ((p - 97) + key) % 26;
                printf("%c", c);
            }
            else
            {
                printf("%c", p);
                j--;
            }
        }
    }
    printf("\n");
}    


//define shift function
int shift(char c)
{
    int i = (int) c;
    while (islower(i))
    {
        i = toupper(i);
    }
    
    i = i - 65;
    return i;
}
