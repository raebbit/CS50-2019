// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

// pointer for current node
node *current_node;


// hash the letter to put into children
unsigned int hash(const char c)
{
    if (c == '\'')
    {
        return 26;
    }
    else
    {
        return tolower(c) - 'a';
    }
}

// Free nodes , for unload function
bool freenode(node *ptr)
{
    for (int i = 0; i < N; i++)
    {
        if (ptr->children[i] != NULL)
        {
            freenode(ptr->children[i]);
        }
    }
    free(ptr);
    return true;
}

// Initializes the counter of words for size function
unsigned int word_count = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
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

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        current_node = root; // should be within while loop.
        //so it starts at the root for every new word.

        for (int j = 0; j < strlen(word); j++)
        {
            int i = hash(word[j]);

            if (current_node->children[i] == NULL)
            {
                // Need to initialize the memory returned from malloc
                // by assigning NULL to all array elements
                // and set is_word to false. (cf. line 64~72)
                current_node->children[i] = malloc(sizeof(node));
                current_node = current_node->children[i];
                if (current_node == NULL)
                {
                    return false;
                }
                current_node->is_word = false;
                for (int n = 0; n < N; n++)
                {
                    current_node->children[n] = NULL;
                }

            }
            else
            {
                current_node = current_node->children[i];
            }
        }

        current_node->is_word = true;
        word_count++;
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
    current_node = root;

    // traversing a trie
    for (int j = 0; j < strlen(word); j++)
    {
        int i = hash(word[j]);
        if (current_node->children[i] == NULL)
        {
            return false;
        }
        else
        {
            current_node = current_node->children[i];
        }
    }

    // Once at end of input word, check if is_word is true
    if (current_node->is_word == true)
    {
        return true;
    }

    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if (word_count == 0)
    {
        return false; // cause it means 'unloaded'
    }
    else
    {
        freenode(root);
    }

    return true;
}
