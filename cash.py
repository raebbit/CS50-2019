from cs50 import get_float


def main():
    d = get_non_negative("Change owed: ")
    c = round(d * 100)

    # quarters
    q = c // 25
    remainder_1 = c % 25

    # dimes
    m = remainder_1 // 10
    remainder_2 = remainder_1 % 10

    # nickels
    n = remainder_2 // 5

    # pennies
    p = remainder_2 % 5

    print(q + m + n + p)


def get_non_negative(prompt):
    while True:
        x = get_float(prompt)
        if x >= 0:
            break
    return x


if __name__ == "__main__":
    main()