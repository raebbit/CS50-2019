from cs50 import get_string
import sys


def main():

    if len(sys.argv) != 2:
        print("Usage: python bleep.py dictionary")
        sys.exit(1)

    words = set()  # empty set for the list of words from dictionary
    file = open(sys.argv[1], "r")  # dictionary

    # stores the words in data structure
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()

    message = get_string("What message would you like to censor?\n")
    msglist = message.split(' ')

    for word in msglist:
        if word.lower() in words:
            for c in word:
                print('*', end='')
        else:
            print(word, end='')
        print('', end=' ')

    print()


if __name__ == "__main__":
    main()
