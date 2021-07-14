import math
import time

from primes import miller_rabin
from prng import LCG, BBS


TRACE = False
MAGS  = [40,  56,  80,  128, 168, 224, 256, 512, 1024, 2048, 4096]
NUMS  = [100, 100, 100, 100, 100, 64,  32,  16,  8,    4,    2]

def gen_primes(bits, num, prime_test, generator):
    """Generates num primes of magnitude bits and records the average time
       necessary to generate each."""
    primes = []
    start_time = time.time()
    for _ in range(num):
        done = False
        n = None
        while not done:
            n = generator.next(bits)
            done = prime_test(n, 40)
        if TRACE:
            print("Found prime of {} bits n={}".format(bits,n))
        primes.append(n)
    return (primes, (time.time()-start_time)/num)


def gen_primes_MR_LCG():
    """Generates prime numbers using a combination of the Linear Congruential Generator
       and the Miller-Rabin primality test.
    """
    PARAMS = {
        # Bits: (Seed, A, B, N)
        40:   (2**40,   2**2-1,   12345, 2**41),
        56:   (2**56,   2**4-1,   12345, 2**57),
        80:   (2**80,   2**6-1,   12345, 2**81),
        128:  (2**128,  2**8-1,   12345, 2**129),
        168:  (2**168,  2**10-1,  12345, 2**169),
        224:  (2**224,  2**15-1,  12345, 2**225),
        256:  (2**256,  2**30-1,  12345, 2**257),
        512:  (2**512,  2**60-1,  12345, 2**513),
        1024: (2**1024, 2**125-1, 12345, 2**1025),
        2048: (2**2048, 2**250-1, 12345, 2**2049),
        4096: (2**4096, 2**500-1, 12345, 2**4097),
    }

    for i in range(len(MAGS)):
        bits = MAGS[i]
        num = NUMS[i]
        print("Searching for {} {} bit primes...".format(num, bits))
        lcg = LCG(*PARAMS[bits])
        primes, avg = gen_primes(bits, num, miller_rabin, lcg)
        print("Found {} primes of {} bits with an average generation time of {} seconds per prime.".format(num, bits, avg))
        print("The primes were: {}".format(primes))


def gen_primes_Solovay_BBS():
    pass

if __name__=='__main__':
    gen_primes_MR_LCG()