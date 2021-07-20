"""Pseudo-Random Number Generators."""

class LCG:
    def __init__(self, seed, a, b, n):
        self._state = seed
        self._a = a
        self._b = b
        self._n = n

    def next(self, bits):
        done = False
        while not done:
            self._state = (self._a*self._state + self._b) % self._n
            if self._state >= 2**bits:
                done = True
        return self._state


class BBS:
    def __init__(self, seed, n):
        self._state = seed
        self._n = n

    def _next_int(self, bits):
        integer = 0
        for _ in range(bits):
            self._state = pow(self._state, 2, self._n)
            integer <<= 1
            integer |= (self._state & 1)
        return integer

    def next(self, bits):
        done = False
        n = None
        while not done:
            n = self._next_int(bits)
            if self._state >= 2**bits:
                done = True
        return n


class ICG:
    def __init__(self, seed, a, b, q):
        self._state = seed
        self._a = a
        self._b = b
        self._q = q

    def next(self, bits):
        done = False
        while not done:
            if self._state == 0:
                self._state = self._b
            else:
                self._state = (self._a*pow(self._state,-1,self._q) + self._b) % self._q
            if self._state >= 2**bits:
                done = True
        return self._state
