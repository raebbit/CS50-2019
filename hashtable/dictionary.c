// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Initializes the counter of words for size function
unsigned int word_count = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // malloc a node pointer for each new word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }
        else
        {
            // copy word into node
            strcpy(new_node -> word, word);
            new_node -> next = NULL;

            // initialize which bucket the word be in
            int bucket = hash(word);

            // insert into a linked list
            // I got a help on this. This solves every problem I had....how? why?
            if (hashtable[bucket] == NULL)
            {
                hashtable[bucket] = new_node;
                word_count++;
            }
            else
            {
                new_node -> next = hashtable[bucket];
                hashtable[bucket] = new_node;
                word_count++;
            }
        }
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    char wordcopy[strlen(word) + 1];
    strcpy(wordcopy, word);

    // traversing linked list
    int bucket = hash(word);

    node *cursor = hashtable[bucket];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor -> word, wordcopy) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor -> next;
        }
    }

    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    //if the word_count is 0, that means it is not loaded
    if (word_count == 0)
    {
        return false;
    }

    // freeing all linked list
    for (int i = 0; i < N; i++)
    {
        node *cursor = hashtable[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor -> next;
            free(temp);
        }
    }

    return true;
}
