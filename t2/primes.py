"""Prime tests."""
import random


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

        # n=1 or n=n-1 trivially satisfy some of the congruences, so we exclude them.
        a = random.randint(2,n-2)
        x = pow(a,d,n)
        if x == 1 or x == n-1:
            continue

        passed = False
        for _ in range(s-1):
            x = pow(x,2,n)
            if x == n-1:
                passed = True

        if passed:
            continue
        else:
            return False

    return True


def fermat(n, k):
    """Probabilistic primality test as described in Wikipedia.

    Refs
    ----
        https://en.wikipedia.org/wiki/Fermat_primality_test
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
        # If n is prime, then it will satisfy the following congruence (Fermat's little thm)
        #
        #   a^(n-1) = 1 (mod n), for all a s.t. 0 < a < n
        #
        # A composite may satisfy this congruence, making it a Fermat pseudo-prime. That is why we run the
        # test multiple times. The goal is thus to find a witness to the compositeness of n; i.e., a nonzero
        # a s.t. n does not satisfy the congruence. A result states that having fixed n, at least half of the
        # numbers a in the range (0,n) which are coprime to n are witnesses (ignoring charmichel numbers).
        # This means that the method gets worse the more composite n is.

        # n=1 or n=n-1 trivially satisfy the congruence, so we exclude them.
        a = random.randint(2,n-2)
        x = pow(a,n-1,n)
        if x == 1:
            continue
        else: # Found a witness
            return False
    return True
