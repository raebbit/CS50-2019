from cs50 import get_int


# get a credit card number from user
ccn = get_int("Number: ")

# get sum by using Luhn's algorithm
sum_1 = 0
sum_2 = 0
for i in range(2, 17, 2):
    d = (ccn % 10**i) // 10**(i-1)
    d_2 = d * 2
    if d_2 > 9:
        a = d_2 % 10
        b = (d_2 % 100) // 10
        d_2 = a + b

    sum_2 = sum_2 + d_2

for j in range(1, 17, 2):
    p = (ccn % 10**j) // 10**(j-1)

    sum_1 = sum_1 + p

sum_t = sum_1 + sum_2

if not sum_t % 10 == 0:
    print('INVALID')
else:
    # valid cards by company
    digit = len(str(ccn))
    set_AMEX = set(['34', '37'])
    set_MASTER = set(['51', '52', '53', '54', '55'])

    if digit == 15 and str(ccn // 10**13) in set_AMEX:
        print('AMEX')
    if digit == 16:
        if str(ccn // 10**14) in set_MASTER:
            print('MASTERCARD')
        if ccn // 10**15 == 4:
            print('VISA')
    if digit == 13 and ccn // 10**12 == 4:
        print('VISA')
