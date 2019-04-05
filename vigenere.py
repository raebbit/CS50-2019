from cs50 import get_string
import sys


def main():
    # get the keyword correctly
    if len(sys.argv) != 2:
        print("Usage: python vigenere.py k")
        sys.exit(1)
    else:
        for l in sys.argv[1]:
            if l.isalpha() == False:
                print("Usage: python vigenere.py k")
                sys.exit(1)

    # get the plaintext
    text = get_string("plaintext: ")
    print("ciphertext: ", end="")

    # using index inside the for loop to iterate key
    index = 0
    secret_word = sys.argv[1].upper()

    # encipher
    for p in text:
        key = ord(secret_word[index % len(secret_word)]) - 65
        if p.isalpha() == True:
            pc = ord(p)
            if p.isupper() == True:
                c = 65 + ((pc - 65) + key) % 26
                index = index + 1
                print(chr(c), end="")
            elif p.islower() == True:
                c = 97 + ((pc - 97) + key) % 26
                index = index + 1
                print(chr(c), end="")

        else:
            print(p, end="")

    print()


if __name__ == "__main__":
    main()
