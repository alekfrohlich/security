import math
import time
from Crypto.Util import number
import itertools

from primes import miller_rabin, fermat
from prng import LCG, BBS


TRACE = False
MAGS  = [40,  56,  80,  128, 168, 224, 256, 512, 1024, 2048, 4096]
NUMS  = [100, 100, 100, 100, 100, 64,  32,  16,  8,    4,    2]


def gen_primes(bits, num, prime_test, generator, rounds_of_prime_test=40):
    """Generates num primes of magnitude bits and records the average time
       necessary to generate each."""
    primes = []
    start_time = time.time()
    for _ in range(num):
        done = False
        n = None
        while not done:
            n = generator.next(bits)
            done = prime_test(n, rounds_of_prime_test)
        if TRACE:
            print("Found prime of {} bits n={}".format(bits,n))
        primes.append(n)
    return (primes, (time.time()-start_time)/num)


def gen_prnumbers(bits, num, generator):
    """Generates num pseude-random numbers of magnitude bits and records the average
       time necessary to generate each."""
    prnumbers = []
    start_time = time.time()
    for _ in range(num):
        prnumbers.append(generator.next(bits))
    return (prnumbers, (time.time()-start_time)/num)


if __name__=='__main__':
    PARAMS_LCG = {
        # The LCG has full modulus (N) when the following conditions are met
        #   1. gcd(B,N) = 1
        #   2. A-1 is divisible by all prime factors of N (that's why it is easy to choose N to be a power of two)
        #   3. A-1 is divisible by 4.
        # For every magnitude, I've fixed N to be the next power of two, chosen an arbitrary odd integer (12345) as B, and chosen
        # A to be such that A = 4t+1.
        # Bits: (Seed, A, B, N)
        40:   (2**40,   2**2+1,   12345, 2**41),
        56:   (2**56,   2**4+1,   12345, 2**57),
        80:   (2**80,   2**6+1,   12345, 2**81),
        128:  (2**128,  2**8+1,   12345, 2**129),
        168:  (2**168,  2**10+1,  12345, 2**169),
        224:  (2**224,  2**15+1,  12345, 2**225),
        256:  (2**256,  2**30+1,  12345, 2**257),
        512:  (2**512,  2**60+1,  12345, 2**513),
        1024: (2**1024, 2**125+1, 12345, 2**1025),
        2048: (2**2048, 2**250+1, 12345, 2**2049),
        4096: (2**4096, 2**500+1, 12345, 2**4097),
    }
    # print("Generating pseudo-random numbers using LCG...")
    # for i in range(len(MAGS)):
    #     bits = MAGS[i]
    #     num = 1000
    #     lcg = LCG(*PARAMS_LCG[bits])
    #     prnumbers, avg = gen_prnumbers(bits, num, lcg)
    #     print("Found {} pseudo-random numbers of {} bits with an average generation time of {} seconds per number.".format(num, bits, avg))
    #     # print("The numbers were: {}".format(prnumbers))

    # print("Generating prime numbers using LCG and MR...")
    # for i in range(len(MAGS)):
    #     bits = MAGS[i]
    #     num = NUMS[i]
    #     print("Searching for {} {} bit primes...".format(num, bits))
    #     lcg = LCG(*PARAMS_LCG[bits])
    #     primes, avg = gen_primes(bits, num, miller_rabin, lcg)
    #     print("Found {} primes of {} bits with an average generation time of {} seconds per prime.".format(num, bits, avg))
    #     # print("The primes were: {}".format(primes))

    # PARAMS_BBS = {
    #     40:   (2**40  +1, 557591*1999651),
    #     56:   (2**56  +1, 258385643*528902719),
    #     80:   (2**80  +1, 1097390420627*2059058134559),
    #     128:  (2**128 +1, 17524145660797552039*36404151453759571543),
    #     168:  (2**168 +1, 19219788008902711173207811*38257294667594570657535847),
    #     224:  (2**224 +1, 5109209828529545593772301224626783*10353939228632702177151328883533811),
    #     256:  (2**256 +1, 334413190550191546685468218391069411071*680297589070506213293537199796293241307),
    #     512:  (2**512 +1, 115738295998969986805678279991843981526673043784370161382827053902293308512039*230830802059811370513355469341276114808962187188384734126025340150456191365847),
    #     1024: (2**1024-1, 13239107774483681539454466274884939134427137787084202962339952604897503691107189107754341799340957174096556075411802863742924161006704560924574663412586259*26603490874191220625697416685892893884126625421819541886389830910701722010366451218932923558528527880222613001518735104933169724825505874586766883407156807),
    #     2048: (2**2048+1, 171977285360112618221033510767303902503809544767464083358700507150439699360759257871078289413433598141270485227701301888768700417828497151807263147925793066143130910266545456602326039020683831000675998700891716874526334308284836052518973369816808958367982066591005668506704697125522520556208480197177824212423*359301480839642386601045976148888129277245635737738973023324383962470731091828726713032735946993023831378720839867294989396341963167626442790539135076049413473864412001090078810716654656495632479880972573540178907529402641497510795003966696711252348696013586023205543507567971746036909120553981054482764994059),
    #     4096: (2**4096+1, 31431948043107356442678195068666257359599515143369443358810113289846998696720285535509170006824409685142784609164109806662111430780804474396437630595688355041237114810822403260850250046534123272538231095643870118696869685323544661585622842191806377208668210257041806683766365539531310577797391990666222309904557329075058425542824862285437271663034080349824521513727011550027493116417208130965271429770829433877445952663772440635996412877173922266991619377382930420665882719662026112597246316293140671920652003564594913806969013034350251517547120998644303666111619110915877611681439986667530898061003647049285747602171*64373013172433144696138175739331267421707486895821184322062513044899431134988239776508805591555709353664985815105532169438065815880910235198454905348544038286489674667671615281014045287850174186172163890700802261686111973534716761042143156771209995737257865465605492509142383934143590367736045833718617538425077262141295383152611703669515809208118249600978725944719305023660026043039831101495819866054695884838965044698645862672805217109793299329284304179089284150641292711774343223277609391009677741445545226203851186233858675021344808370128500896710896849483426805896458394205708461890248569932208040359003339920623),
    # }
    # print("Generating pseudo-random numbers using BBS...")
    # for i in range(len(MAGS)):
    #     bits = MAGS[i]
    #     num = 10
    #     bbs = BBS(*PARAMS_BBS[bits])
    #     prnumbers, avg = gen_prnumbers(bits, num, bbs)
    #     print("Found {} pseudo-random numbers of {} bits with an average generation time of {} seconds per number.".format(num, bits, avg))
    #     # print("The numbers were: {}".format(prnumbers))

    # bits = 56
    # num = 1000
    # lcg = LCG(*PARAMS_LCG[bits])
    # primes, avg = gen_primes(bits, num, miller_rabin, lcg)
    # print("Found {} primes of {} bits with an average generation time of {} seconds per prime.".format(num, bits, avg))
    ps = []
    qs = []
    bits = 4096
    l = bits//2
    for _ in range(100):
        ps.append(number.getPrime(l))
        qs.append(number.getPrime(l+1))
    good_ps = []
    good_qs = []
    for p in ps:
        if (p % 4) == 3:
            good_ps.append(p)
    for q in qs:
        if (q % 4) == 3:
            good_qs.append(q)

    for (p,q) in itertools.product(good_ps, good_qs):
        g = math.gcd((p-3)//2, (q-3)//2)
        if g == 2 and math.log(p*q,2) > bits+0.9:
            print((p,q))
            print(g)
            print(math.log(p*q,2))
            # break
        # 73113891254340439 91670373153188623