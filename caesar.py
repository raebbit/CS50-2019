import sys
from cs50 import get_string


# get the key
if len(sys.argv) != 2:
    print("Usage: python caesar.py k")
    sys.exit(1)
else:
    for l in sys.argv[1]:
        if l.isdigit() == False:
            print("Usage: python caesar.py k")
            sys.exit(1)

key = int(sys.argv[1])

# get the plaintext
text = get_string("plaintext: ")
print("ciphertext: ", end="")

# encipher
# p is string, c is integer
for p in text:
    pc = ord(p)
    if p.isupper() == True:
        c = 65 + ((pc - 65) + key) % 26
        print(chr(c), end="")
    elif p.islower() == True:
        c = 97 + ((pc - 97) + key) % 26
        print(chr(c), end="")
    else:
        print(p, end="")

print()

