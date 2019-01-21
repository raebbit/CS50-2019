#define _XOPEN_SOURCE
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int brute_force(string hash);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }
    else
    {
        string key = NULL;
        string hash = argv[1];
        brute_force(hash);
        return 0;
    }
}

//cracking hash by brute force algorithm
int brute_force(string hash)
{
    char salt[3];
    strncpy(salt, hash, 2);  //salt is the first two chars of hash
    salt[2] = '\0';
    
    char pkey1[2];
    pkey1[1] = '\0'; //possible key, 1 chars
    
    for (pkey1[0] = 'A'; pkey1[0] <= 'z'; pkey1[0]++)
        if (strcmp(hash, crypt(pkey1, salt)) == 0)
        {
            printf("%s\n", pkey1);
            return 0;
        }
    
    char pkey2[3];
    pkey2[2] = '\0'; //possible key, 2 chars
    
    for (pkey2[0] = 'A'; pkey2[0] <= 'z'; pkey2[0]++)
        for (pkey2[1] = 'A'; pkey2[1] <= 'z'; pkey2[1]++)
            if (strcmp(hash, crypt(pkey2, salt)) == 0)
            {
                printf("%s\n", pkey2);
                return 0;
            }
    
    char pkey3[4];
    pkey3[3] = '\0'; //possible key, 3 chars
    
    for (pkey3[0] = 'A'; pkey3[0] <= 'z'; pkey3[0]++)
        for (pkey3[1] = 'A'; pkey3[1] <= 'z'; pkey3[1]++)
            for (pkey3[2] = 'A'; pkey3[2] <= 'z'; pkey3[2]++)
                if (strcmp(hash, crypt(pkey3, salt)) == 0)
                {
                    printf("%s\n", pkey3);
                    return 0;
                }
    
    char pkey4[5];
    pkey4[4] = '\0'; //possible key, 4 chars
    
    for (pkey4[0] = 'A'; pkey4[0] <= 'z'; pkey4[0]++)
        for (pkey4[1] = 'A'; pkey4[1] <= 'z'; pkey4[1]++)
            for (pkey4[2] = 'A'; pkey4[2] <= 'z'; pkey4[2]++)
                for (pkey4[3] = 'A'; pkey4[3] <= 'z'; pkey4[3]++)
                    if (strcmp(hash, crypt(pkey4, salt)) == 0)
                    {
                        printf("%s\n", pkey4);
                        return 0;
                    }
    
    char pkey5[6];
    pkey5[5] = '\0'; //possible key, 5 chars
    
    for (pkey5[0] = 'A'; pkey5[0] <= 'z'; pkey5[0]++)
        for (pkey5[1] = 'A'; pkey5[1] <= 'z'; pkey5[1]++)
            for (pkey5[2] = 'A'; pkey5[2] <= 'z'; pkey5[2]++)
                for (pkey5[3] = 'A'; pkey5[3] <= 'z'; pkey5[3]++)
                    for (pkey5[4] = 'A'; pkey5[4] <= 'z'; pkey5[4]++)
                        if (strcmp(hash, crypt(pkey5, salt)) == 0)
                        {
                            printf("%s\n", pkey5);
                            return 0;
                        }
    return 1;
}
