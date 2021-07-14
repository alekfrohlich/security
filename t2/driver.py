import math
import random
from prng import LCG

# def fast_mexp(x,e,n):
#     """x^e (mod n)."""
#     if n == 0:
#         return 1
def f(x,e,m):
    X = x
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E // 2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y


def miller_rabin(n,k):
    """Probabilistic primality test as described in Wikipedia.

    Refs
    ----
        https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    """
    # Easy cases
    if n == 1:
        return False
    if n == 2:
        return True
    if (n % 2) == 0:
        return False

    # Factor n = d*2^s+1, where d is odd
    s = 0 ; d = n-1
    while (d % 2) == 0:
        d = d // 2
        s += 1
    # print("n = {}*2^{}+1".format(d,s))
    # print(s)

    # Perform the test k times
    for __ in range(k):
        # If n is prime, then at least one of the following tests will recognize it:
        #
        #   1) a^d = 1 (mod n)
        #   2) a^(d*2^r) = n-1 (mod n), for some 0 <= r < s
        #
        # For each round, at most r congruences are checked. If all fail, then n is composite.
        # However, a congruence holding does not imply n is prime as n may be a false witness w.r.t the base a.
        # Luckly, a number n is typically not a false witness to many different basis. Hence, we repeat the test
        #   multiple times to incrise our confidence in the primality of n.
        # print(__)
        a = random.randint(2,n-2)
        # x = a**d % n
        x = f(a,d,n)
        # print("a={}".format(a)) ; print("x={}".format(x))
        if x == 1 or x == n-1:
            continue

        passed = False
        for _ in range(s-1):
            # x = (x*x) % n
            x = f(x,2,n)
            if x == n-1:
                passed = True

        if passed:
            continue
        else:
            return False

    return True

if __name__=='__main__':
    # Random numbers of magnitude: 40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096 bits

    # 2048
    A = 2**250 - 1
    B = 12345
    N = 2**2049
    lcg = LCG(2**2048,A,B,N)
    done = False
    n = None
    while not done:
        n = lcg.next(2048)
        # print(n)
        done = miller_rabin(n,40)
    print("Found the 2048-bit prime n={}".format(n))

    # 4096
    A = 2**500-1
    B = 12345
    N = 2**4097
    lcg = LCG(2**4096,A,B,N)
    done = False
    n = None
    while not done:
        n = lcg.next(4096)
        # print(n)
        done = miller_rabin(n,40)
    print("Found the 4096-bit prime n={}".format(n))