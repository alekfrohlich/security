""""""

class LCG:
    def __init__(self,seed,a,b,n):
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

class LFSR:
    def __init__(self,):
        pass

