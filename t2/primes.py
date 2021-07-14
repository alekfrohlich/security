""""""
import random


def fast_exp(x, e, m):
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

        a = random.randint(2,n-2)
        x = fast_exp(a,d,n)
        # print("a={}".format(a)) ; print("x={}".format(x))
        if x == 1 or x == n-1:
            continue

        passed = False
        for _ in range(s-1):
            x = fast_exp(x,2,n)
            if x == n-1:
                passed = True

        if passed:
            continue
        else:
            return False

    return True


def jacobi(a, n):
    """Computes the Jacobi Symbol (a/n), except that -1 is returned as n-1."""


def solovay_strassen(n, k):
    """Probabilistic primality test as described in Wikipedia.

    Refs
    ----
        https://en.wikipedia.org/wiki/Solovay%E2%80%93Strassen_primality_test
    """
    # Easy cases
    if n == 1:
        return False
    if n == 2:
        return True
    if (n % 2) == 0:
        return False

    # Perform the test k times
    for __ in range(k):
        a = random.randint(2, n-1)
        x = jacobi(a, n)

        if x == 0 or fast_exp(a, (n-1)//2, n) != x:
            return False
    return True