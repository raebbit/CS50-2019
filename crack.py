import sys
import crypt
import string


def main():
    # get a hashed password
    if len(sys.argv) != 2:
        sys.exit("Usage: python crack.py hash")

    else:
        hashed_pw = sys.argv[1]
        brute_force(hashed_pw)


def brute_force(hashedword):
    salt = hashedword[:2]  # salt is a first two chars of hashed password
    lts = string.ascii_letters
    lena = len(string.ascii_letters)
    key = ""  # empty string

    for u in range(lena):
        for w in range(lena):
            for z in range(lena):
                for y in range(lena):
                    for x in range(lena):
                        if crypt.crypt(key, salt) == hashedword:
                            print(key)
                            sys.exit(0)
                        key = lts[x] + key[1:]
                    key = key[:1] + lts[y] + key[2:]
                key = key[:2] + lts[z] + key[3:]
            key = key[:3] + lts[w] + key[4:]
        key = key[:4] + lts[u]


if __name__ == "__main__":
    main()
