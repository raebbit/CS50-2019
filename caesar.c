#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            int a = argv[1][i];
            if (isdigit(a) == 0)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }          
    }
    
    int key = atoi(argv[1]);
    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    
    //encryption 
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        //preserve case,space,punctuation
        int p = (int) text[i];
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
        }
    }
    printf("\n");
}
   
   
