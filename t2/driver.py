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
    #     56:   (2**56  +1, 226770751*487153111),
    #     80:   (2**80  +1, 73113891254340439*91670373153188623),
    #     128:  (2**128 +1, 340282366920938463463374659835025145401*509126080944614503374156838505530497337),
    #     168:  (2**168 +1, 691463123470990757152655659793423689541448921377849*680514537863828357127424684016649260214154203943993),
    #     224:  (2**224 +1, 35608696065441588290938341126366558678974373585661280879692741587001*30080160041925342447545961041311446404884154381681348631054489137209),
    #     256:  (2**256 +1, 137603816109809074067575235761529420158636010768437423997952976594557611290681*177474564031781104902291724798769506022311090289393904907323418957980909973561),
    #     512:  (2**512 +1, 13409233835419182183762550213395150442144840979302283726132365170593933040769308601594507464072560321108156426677528457543397182644925524059062666952454201*17506668012316419832633918601407756736696139050167370273989740989384448738896284497229636375441746771498118459102861080709655182935605870439825637579436089),
    #     1024: (2**1024-1, 209725543907854497422145632562088298140032359174657797566235026984857000959868694039416982067134863888782191593726320729872335496636624386304180931810467397740724602845932839683241654150055993818145060190494220894500577671084543065815595210390093217185240782961577576122939240853171864976741929145969517015097*180467572785190590279252071316612873002352721361300991639653670373888436043809587732350148347716340346148775878091195561015938251479948346792296793435560348742689103939057968464493522068018374168707540889221999994651647585582181903869168946857377713691969155813104916802225961591896276103687975426809493729337),
    #     2048: (2**2048+1, 32317018144446037666975372877824726781524852878860633132444153889363002590845065337388407232210840726496080521888695242452598336837460478559147397139115747324905252508562552944499418592980655180720126667479170251867457344037061464088588414440155571783916596272371596911536323015193621747110601620001113873852221241488399332965674656970171114516464235661657581333478068801424051401951197941197800904323152805756728524147367484355333935502633059227749036685835525533649936852963854524309444584629106540337129257238197347753985426741731579762366051622826614595825597788665652078151799041396467367905673434489658735079481*62884676495405970369236750628719595747926233701658033084604644870536114967450196393783362016707554253969626716798829871310314825711418946249831054285893792156965774432985394043187962257088622449979166845490712946462325378926619912242378354217545078980515382304791247432607652548482067243289373453841826288539489032214285178729126556957007211715779411257862033062178788853787780014898326917019558279644078437031906780600069889754132990123268063475429182778068468069426509384504379045208400820350540067696886309978626341121403099567092967330558647948757981733625009862639017229350947655192484299687488222357950809780281),
    #     4096: (2**4096+1, 1070195344011235349253151788793639651912486051503763304607199145200798602235726059076403025244582929576427117698895580310199411211818768649680447451045819574851401064611228415301300857788799018990976949815190456153073261901745214514482290556243861886912018499240438381259766607150640517854627222328399291215289084077515451737492342374086909843155537332257287569293752397579035472977825944312652105640399129190302191220838031506803984748022409810061901260503864312666327163343339191935631512163356394835241703947854213787427811656036130279902961290533070527276719178094960133951541488138360793276457203918904664212119138402021228563267482570804126598283157174377157686598636343895136582783854047277799095509367533374454011186120146763122120706377587898444137005612399833564596932799337233252471645272105470227324655466283873615609184988693829559316281277945184066677272145591135981991962772590693114111334061660100617230504077196850163409441434646320449218106600081702649613092349520207993150956608742130439341460334866556353921815993043320923349457006750899254810994307903738272198859007764683114345201146618725383268229235305011838749650015047521442652620867367799032378658632548824703666693954441114646641974615720026793596982145081*1196032456791661554366574581518815013156368660134482722529634819174627658729923751279552644770247867352979761460040517306434822189420842414569927907922809105676601730136931737719846292128135317970846780935693167078525110344939046248463093312831223481211074343462510598663387091488146930020818304699757196488717882819003348319443194758944340758144700712908449259302003007363528648812131170666170915496499938206904617057511013608368827963615940474748825928871422695977578035447320918464139628016070800401656380352430001679963166385380835300396775746416499065133286640650759973565196322689123460340655721575776773154003062222930663917134937711856767689092144908009615242825789386030688823308915675377760982976351476976869315082610546814943122231351502137364873889940242961426540205345153112720989819461599606075337865527901888958811736877156275625534992967584276993843515575582899380623881106262550585781070343809706490685428379553756799584394874175727045595786566002305551110495519252719715101678457984105465569128816391217090859173783241750093397330050490261489414239017250307394782452060823078603933239693846239181916025574275772848671865354278250738834857707110837171218243821139659930005353456509251016707746743945916456806232633401),
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
    bits = 56
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
        if g == 2 and math.log(p*q,2) > bits+0.5:
            print((p,q))
            print(g)
            print(math.log(p*q,2))
            # break
        # 73113891254340439 91670373153188623