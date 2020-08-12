from scipy import special
import delay.calculator as calc
from delay.strategy import *
from collections import deque
import matplotlib.pyplot as plt


def P(n, r, p):
    if (n+r) % 2:
        return 0.0
    if 0 <= 1/2*(n+r) <= n:
        return 0.0
    w = 1/2*(n+r)
    ww = 1/2*(n-r)
    return special.binom(n, w) * p**w * (1-p)**(ww)


def generalProb(d, epsilon, val, N, shiftA, shiftB):
    calculateProb = calc.step(d=d, epsilon=epsilon)
    fA = fA_Hard(N)
    fB = fB_Hard(N)
    return calculateProb(fA(val+shiftA) - fB(val+shiftB))
    

def veryGeneralProb(val, d, epsilon):
    if val > d:
        return epsilon
    return 0.5


def psi(d, epsilon, x, N, tauA, r):
    if (tauA+r) % 2:
        return 0.0
    w = 1/2*(tauA+r)
    if not 0 <= w <= tauA:
        return 0.0
    comb = special.binom(tauA, w)
    return comb * generalProb(d, epsilon, x, N, r, 0)


def paths(tauA, r):
    if (tauA+r) % 2:
        return 0.0
    w = 1/2*(tauA+r)
    
    return special.binom(tauA, w)


def domain(N):
    return range(-int(N/2), int(N/2)+1)


def fineGrainedProbabilities(x, N, tauA, r, probabilities):
    if (tauA+r) % 2:
        return 0.0
    if not -N/2 <= x+r <= N/2:
        return 0.0
    w = 1/2*(tauA+r)
    if not 0 <= w <= tauA:
        return 0.0

    def multiply(pos, tau, destination):
        def canDecrement(pos, tau, destination):
            if pos >= destination:
                return pos-1 >= -N/2
            return destination-(pos-1) <= tau-1 and pos-1 >= -N/2

        def canIncrement(pos, tau, destination):
            if pos <= destination:
                return pos+1 <= N/2
            return pos+1-destination <= tau-1 and pos+1 <= N/2

        if tau == 0:
            return 1.0
        
        accumulator = 0.0
        if canDecrement(pos, tau, destination):
            accumulator += (1-probabilities[pos]) * \
                multiply(pos-1, tau-1, destination)
        if canIncrement(pos, tau, destination):
            accumulator += probabilities[pos] * \
                multiply(pos+1, tau-1, destination)

        return accumulator
    
    destination = x+r
    
    return multiply(x, tauA, destination)


def index(x, N):
    return int(x + N/2)


def isRAccessible(r, N, tauA, x):
    if (tauA+r) % 2:
        return False
    if not -N/2 <= x+r <= N/2:
        return False
    w = 1/2*(tauA+r)
    if not 0 <= w <= tauA:
        return False
    return True


def accurateProbabilities(x: int, N, tauA, rightProbs, stationaryProbs, d, epsilon):
    def inorder(depth, current: int):
        current = int(current)
        if depth == tauA:
            return (modelRightProbability(d, epsilon, current) * stationaryProbs[current], stationaryProbs[current])
        leftProb = 1-rightProbs[current]
        rightProb = rightProbs[current]

        leftInorder = inorder(depth+1, current-1)
        rightInorder = inorder(depth+1, current+1)
        return np.add(np.multiply(leftInorder, leftProb), np.multiply(rightInorder, rightProb))

    nomin, denomin = inorder(0, x)
    return nomin / denomin


def eigenvector(p):
    n = len(p)
    evector = deque()
    evector.appendleft(1)
    quotient = [p[1]]
    quotient[0] /= (1-p[0])
    for i in range(2, n):
        q = quotient[i-2]
        quotient.append(p[i]/(1-(1-p[i-2])*q))

    return quotient


def normalize(vec):
    s = np.sum(vec)
    return list(np.array(vec)/s)


def calculateStationary(quotient):
    """
    quotient - vector of matrix elements built up from the (1,1) element and
    the elements on the diagonal (2,1)…(n,n-1)
    """
    evector = deque()
    evector.appendleft(1)
    n = len(quotient)
    for i in range(n-1, -1, -1):
        evector.appendleft(quotient[i] * evector[0])
    return normalize(evector)


def probabilities2Stationary(probs):
    """
    probs - probabilities of goring right
    """
    for i in range(0, len(probs)):
        probs[i] = 1-probs[i]
    stationary = eigenvector(probs)
    stationary = calculateStationary(stationary)
    for i in range(0, len(probs)):
        probs[i] = 1-probs[i]
    return stationary


def plot(arr, N=None):
    if not N:
        N = len(arr)-1
    plt.plot(domain(N), arr)
    plt.show()


def domainDict(arr):
    N = len(arr)-1
    return dict(zip(domain(N), arr))


def expectedValue(stationary, N=None):
    if not N:
        N = len(stationary)-1
    ev = 0.0
    for i in range(int(-N/2), int(N/2+1)):
        ev += i * stationary[index(i, N=N)]
    return ev


def domainDFDict(arr):
    N = len(arr)-1
    return {'x': domain(N), 'values': arr}


def makeNonDeterministic(probs):
    N = len(probs)
    for i in range(0, N):
        if probs[i] != probs[i]: # nan
            if i < N/2:
                probs[i] = 0.9999
            else:
                probs[i] = 0.0001
        elif probs[i] < 1e-4:
            probs[i] = 0.0001
        elif probs[i] > 1-1e-4:
            probs[i] = 0.9999


def rightProbabilities(stationaryProbs, rightProbs, epsilon, d, tau, N=None):
    if not N:
        N = len(stationaryProbs)-1

    rp = []

    x = -N/2
    while x <= N/2:
        if x < -d:
            rp.append(1-epsilon)
        elif x <= d-tau:
            rp.append(1/2)
        else:
            sumNominator = 0.0
            sumDenominator = 0.0
            r = -tau
            while r <= tau:
                if not isRAccessible(r, N, tau, x):
                    r += 1
                    continue
                
                forcedStepsNumber = abs(r)
                forcedStepsProbability = 1
                for i in range(0, forcedStepsNumber):
                    if r < 0:
                        ind = index(x - i, N)
                        forcedStepsProbability *= 1-rightProbs[ind]
                    else:
                        ind = index(x + i, N)
                        forcedStepsProbability *= rightProbs[ind]

                n = tau - forcedStepsNumber
                middle = x + r/2
                m = index(middle, N)
                prob = forcedStepsProbability
                prob *= (rightProbs[m]) ** (n/2)
                prob *= (1 - rightProbs[m]) ** (n/2)
                
                comb = abs(r) * special.binom(tau-abs(r), 1/2*(tau-abs(r)))
                o = comb * prob
                o *= stationaryProbs[index(x+r, N)]

                sumDenominator += o

                o *= modelRightProbability(d=d, epsilon=epsilon, x=x+r)
                sumNominator += o

                r += 1

            # normalize probability
            rp.append(sumNominator / sumDenominator)

        x += 1

    makeNonDeterministic(rp)
    return rp


def rightProbabilitiesAccurate(stationaryProbs, rightProbs, epsilon, d, tau, N=None):
    if not N:
        N = len(stationaryProbs)-1

    rp = []

    x = -N/2
    while x <= N/2:
        if x < -d:
            rp.append(1-epsilon)
        elif x <= d-tau:
            rp.append(1/2)
        elif x > d+tau:
            rp.append(epsilon)
        else:
            prob = accurateProbabilities(x, N, tau, rightProbs, stationaryProbs, d, epsilon)
            rp.append(prob)

        x += 1

    makeNonDeterministic(rp)
    return rp


def rightProbabilitiesWithSampling(stationaryProbs, rightProbs, epsilon, d, tau, sampleNumber=10, N=None):
    if not N:
        N = len(stationaryProbs)-1

    def index(x):
        return int(x+N/2)

    rp = []

    x = -N/2
    while x <= N/2:
        if x < -d:
            rp.append(1-epsilon)
        elif x <= d-tau:
            rp.append(1/2)
        elif x > d+tau:
            rp.append(epsilon)
        else:
            print('================================')
            print('x=', int(x), sep='')
            sumNominator = 0.0
            sumDenominator = 0.0
            r = -tau
            while r <= tau:
                if not isRAccessible(r, N, tau, x):
                    r += 1
                    continue
                print('\tr=', r, sep='')

                forcedStepsNumber = abs(r)
                forcedStepsProbability = 1
                for i in range(0, forcedStepsNumber):
                    if r < 0:
                        ind = index(x - i)
                        forcedStepsProbability *= rightProbs[ind]
                    else:
                        ind = index(x + i + 1)
                        forcedStepsProbability *= 1-rightProbs[ind]

                k = int((tau - forcedStepsNumber)/2)
                prob = forcedStepsProbability
                left = min(x, x+r)  # left <= right
                right = max(x, x+r)
                leftMost = left-k  # leftMost < rightMost
                rightMost = right+k
                leftMost = int(max(leftMost, -N/2))
                rightMost = int(min(rightMost, N/2))
                sampleDict = {
                    'left': leftMost,
                    'right': rightMost,
                    'k': k,
                    'rp': rightProbs,
                    'index': index
                }

                # lProb, rProb = sampleEdges(sampleDict)
                # prob *= lProb * rProb
                # lProb, rProb = sampleEdgesInverse(sampleDict)
                # prob *= lProb * rProb
                lProb, rProb = sampleTimes(sampleNumber, sampleDict)
                print('\t\t', round(lProb, 3), '        ', round(rProb, 3), sep='')
                prob *= lProb * rProb

                comb = abs(r) * special.binom(tau-abs(r), 1/2*(tau-abs(r)))
                print('\t\to = ', comb, ' * ', round(prob*1000, 3), sep='')
                o = comb * prob
                o *= stationaryProbs[index(x+r)]

                sumDenominator += o

                o *= modelRightProbability(d=d, epsilon=epsilon, x=x+r)
                sumNominator += o
                print('')

                r += 1
            print('================================\n')

            # normalize probability
            rp.append(sumNominator / sumDenominator)

        x += 1

    makeNonDeterministic(rp)
    return rp



def modelRightProbability(d, epsilon, x):
    if x <= -d:
        return 1-epsilon
    if x <= d:
        return 1/2
    return epsilon


def initialStationaryProbabilities(N, epsilon, d):
    probs = []
    i = -N/2
    while i <= N/2:
        if i < -d or i > d:
            probs.append(epsilon/(1 + epsilon*(N-2*d)))
        elif i==-d or i==d:
            probs.append(1/(4*d + 4*epsilon*(N-2*d)*d))
        else:
            probs.append(1/(2*d + 2*epsilon*(N-2*d)*d))
        i += 1
    return probs


def initialRightProbabilities(N, d, epsilon):
    probs = []
    i = -N/2
    while i <= N/2:
        if i < -d:
            probs.append(1-epsilon)
        elif i <= d:
            probs.append(1/2)
        else:
            probs.append(epsilon)
        i += 1
    return probs


def sample(left, right, k, rp, index):
    goLeft = np.random.randint(left+1, right+1, size=k)
    goRight = np.random.randint(left, right, size=k)
    leftProduct, rightProduct = 1.0, 1.0
    print('\t\t\t\t', goLeft, '   ;   ', goRight, sep='')
    for i in range(k):
        leftProduct *= 1-rp[index(goLeft[i])]
        rightProduct *= rp[index(goRight[i])]
        print('\t\t\t\t\t', leftProduct, '   ;   ', rightProduct, sep='')
    return leftProduct, rightProduct


def sampleTimes(number, sampleDict):
    lArray, rArray = [], []
    for i in range(number):
        l, r = \
            sample(
                sampleDict['left'],
                sampleDict['right'],
                sampleDict['k'],
                sampleDict['rp'],
                sampleDict['index']
            )
        print('\t\t\t', l, '       ', r, sep='')
        lArray.append(l)
        rArray.append(r)
    return np.mean(lArray), np.mean(rArray)


def sampleEdges(sampleDict):
    left = sampleDict['left']
    right = sampleDict['right']
    k = sampleDict['k']
    rp = sampleDict['rp']
    index = sampleDict['index']

    if k == 0:
        return 1.0, 1.0
    
    leftEdge = 1-rp[index(left+1)]
    rightEdge = rp[index(right)]

    return np.multiply((leftEdge, rightEdge), sample(left, right, k-1, rp, index))


def sampleEdgesInverse(sampleDict):
    left = sampleDict['left']
    right = sampleDict['right']
    k = sampleDict['k']
    rp = sampleDict['rp']
    index = sampleDict['index']

    if k == 0:
        return 1.0, 1.0

    try:
        leftEdge = 1-rp[index(right+1)]
    except IndexError:
        leftEdge = 1-rp[index(right)]
    rightEdge = rp[index(left)]

    return np.multiply((leftEdge, rightEdge), sample(left, right, k-1, rp, index))
