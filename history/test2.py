from z3 import *

# we guess the correct length of the password through trial and errol# see alternate solution, sol-hasher2.py
wanted_length = 6
names = ['x{}'.format(i) for i in range(wanted_length)]
# chars is a list of symbolic integers
chars = [z3.Int(n) for n in names]

n = 7
n2 = 593779930
# n becomes an accumulated logical formula
# as we keep iterating through this loop
for char in chars:
    print(char)
    n = n * 31 + char
    print(n)
# ret is now a constraint we have to satisfy
ret = (n % (2**32)) == n2
print("-----")
print(ret)

if __name__ == "__main__":
    s = z3.Solver()
    s.add(ret)
    # " limiting each char to only lowercase alphabet gives us"
    # the expocted solution, and since we are using z3.Ints()
    for c in chars:
        s.add(c <= ord('z'))
        s.add(c >= ord('a'))
    if s.check().r != 1:
        print('not sat!')
    else:
        # print('sat!')
        m = s.model()
        print(''.join(chr(m[c].as_long()) for c in chars))