# mario_less
from cs50 import get_int


def main():
    h = get_height("Height: ")
    for i in range(h):
        for j in range(h - (i + 1)):
            print(" ", end="")
        for k in range(i + 1):
            print("#", end="")
        print()


def get_height(prompt):
    # get height between 1 and 8
    while True:
        n = get_int(prompt)
        if n > 0 and n < 9:
            break
    return n


if __name__ == "__main__":
    main()

