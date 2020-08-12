from enum import Enum
import delay.strategy as strategy
import random
import matplotlib.pyplot as plt
import numpy as np
import delay.value


class FunctionType(Enum):
    HARD = 1
    SMOOTH = 2
    HARD_INTERVAL = 3
    SKEW45 = 4,
    HARD_SKEW = 5,
    HARD_SKEW_TO0 = 6


class SimulationPlotter:
    def __init__(self, *args, **kwargs):
        return 

    def plotOnlyHistogram(self, imgFile=None):
        plt.hist(self.x[100*self.conv:],
                 bins=np.linspace(-self.N/2-0.5, self.N/2+0.5, self.N+2))
        print('µ = ', np.mean(self.x[100*self.conv:]))

        if imgFile:
            plt.savefig(imgFile)

        plt.show()

    def plot(self):
        _, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 4.8))
        ax1.plot(self.x)
        (bins, _, _) = ax2.hist(
            self.x[100*self.conv:], bins=np.linspace(-self.N/2-0.5, self.N/2+0.5, self.N+2))
        print('µ = ', np.mean(self.x[100*self.conv:]))


class Simulation(SimulationPlotter):

    def __init__(self, typee: FunctionType, tau, calculateValue, 
                 calculateProbability):
        self.fA = None
        self.fB = None
        self.x = []
        self.typee = typee
        self.N = 100
        self.d = 0
        self.omega = 6
        self.updateStrategies()
        self.tauA = tau[0]
        self.tauB = tau[1]
        self.calculateValue = calculateValue
        self.duration = 0
        self.calculateProbability = calculateProbability
        self.conv = self.N
        self.average = None
        self.iterations = 1

    def getDuration(self):
        return self.duration

    def setDuration(self, duration):
        self.duration = duration

    def getX(self):
        return self.x
    
    def initialize(self):
        m = max(self.tauA, self.tauB)
        self.x = [0] * m + [1]

    def setTau(self, tau):
        self.tauA = tau[0]
        self.tauB = tau[1]

    def getN(self):
        return self.N
    
    def setN(self, N):
        self.N = N
        self.updateStrategies()
        self.conv = N

    def setD(self, d):
        self.d = d
        self.updateStrategies()

    def setConv(self, conv):
        self.conv = conv

    def getOmega(self):
        return self.omega

    def setOmega(self, omega):
        self.omega = omega
        self.updateStrategies()

    def getIterations(self):
        return self.iterations

    def setIterations(self, iterations):
        self.iterations = iterations

    def getAverage(self):
        return self.average

    def updateStrategies(self):
        if self.typee == FunctionType.HARD:
            self.fA = strategy.fA_Hard(N=self.N)
            self.fB = strategy.fB_Hard(N=self.N)
        elif self.typee == FunctionType.SMOOTH:
            self.fA = strategy.fA_Smooth(N=self.N, d=self.d, omega=self.omega)
            self.fB = strategy.fB_Smooth(N=self.N, d=self.d, omega=self.omega)
        elif self.typee == FunctionType.HARD_INTERVAL:
            self.fA = strategy.fA_HardInterval(N=self.N, d=self.d)
            self.fB = strategy.fB_HardInterval(N=self.N, d=self.d)
        elif self.typee == FunctionType.SKEW45:
            self.fA = strategy.fA_Skew45deg(N=self.N, d=self.d)
            self.fB = strategy.fB_Skew45deg(N=self.N, d=self.d)
        elif self.typee == FunctionType.HARD_SKEW:
            self.fA = strategy.fA_HardSkew(N=self.N, d=self.d)
            self.fB = strategy.fB_HardSkew(N=self.N, d=self.d)
        elif self.typee == FunctionType.HARD_SKEW_TO0:
            self.fA = strategy.fA_HardSkewTo0(N=self.N, d=self.d)
            self.fB = strategy.fB_HardSkewTo0(N=self.N, d=self.d)

    def run(self):
        partial_avg = []
        self.initialize()

        for i in range(self.iterations):
            self.crop()

            def nextElem(func):
                term = -self.N/2 if func == max else self.N/2
                rc = self.calculateValue(previousA, previousB)
                value = -rc if func == max else rc
                return func(self.x[current] + value, term)

            current = len(self.x)-1
            try:
                for _ in range(0, self.duration):
                    previousA, previousB = self.fA(self.x[current - self.tauA]), self.fB(self.x[current - self.tauB])
                    
                    prob = self.calculateProbability(previousA - previousB)
                    r = random.random()
                    if r < prob:
                        nextElement = nextElem(min)  # +1
                    else:
                        nextElement = nextElem(max)  # -1
                            
                    self.x.append(nextElement)
                    current += 1
            except IndexError:
                print(self.x)
                print(current)
                print(self.tauA)
                print(self.tauB)

            if i == 0:
                partial_avg.append(np.mean(self.x[100*self.conv:]))
            else:
                partial_avg.append(np.mean(self.x))
            
        self.average = (partial_avg[0] * (self.duration-100*self.conv) + np.sum(
            partial_avg[1:])*self.duration)/(self.duration-100*self.conv + (self.iterations-1)*self.duration)
    
    def crop(self):
        m = max(self.tauA, self.tauB)
        self.x = self.x[:m+2]

    def info(self):
        print("N=%d, τ_A=%d, τ_B=%d, d=%d" % (self.N, self.tauA, self.tauB, self.d))
    
    def systematicInfo(self):
        print(self.d, ', ', self.tauA, ', ', np.mean(self.x[100*self.conv:]))

    def showModelFunctions(self):
        vfA = np.vectorize(self.fA)
        vfB = np.vectorize(self.fB)

        x = np.linspace(-self.N/2, self.N/2, num=self.N)
        yA = vfA(x)
        yB = vfB(x)

        plt.plot(x, yA, label='f_A(x)')
        plt.plot(x, yB, label='f_B(x)')

        plt.legend()
        plt.show()
        

class Direction(Enum):
    LEFT = min
    RIGHT = max


class WarmUpSimulation:

    def __init__(self, epsilon, leftProbability, rightProbability, calculateValue=delay.value.warmUpCalculateValue):
        self.epsilon = epsilon
        self.leftProbability = leftProbability
        self.rightProbability = rightProbability
        self.calculateValue = calculateValue
        self.x = []
        self.N = 100
        self.duration = 0
        self.conv = 100

    def setDuration(self, duration):
        self.duration = duration

    def setN(self, N):
        self.N = N

    def run(self, halfByHalf=True):
        self.initialize()

        def nextElem(func):
            term = -self.N/2 if func == max else self.N/2
            rc = self.calculateValue()
            value = -rc if func == max else rc
            return func(self.x[current] + value, term)

        def chooseNext(direction, prob):
            func = min if direction == Direction.RIGHT else max

            def reverse(func):
                return max if func == min else min
            if random.random() <= prob:  # p(event) = prob
                return nextElem(func)
            else:
                return nextElem(reverse(func))

        current = len(self.x)-1
        for _ in range(0, self.duration):
            previous = self.x[current]

            if previous < 0:
                nextElement = chooseNext(Direction.RIGHT, self.rightProbability)
            elif previous > 0:
                nextElement = chooseNext(Direction.LEFT, self.leftProbability)
            else:
                if halfByHalf:
                    nextElement = chooseNext(Direction.LEFT, 1/2)
                else:
                    r = random.random()
                    if r > self.epsilon:
                        nextElement = previous
                    else:
                        nextElement = chooseNext(Direction.LEFT, 1/2)
                        '''
                        p(A) = epsilon
                        p(B) = 1/2
                        p(A, B) = epsilon * 1/2 = epsilon/2
                        '''

            self.x.append(nextElement)
            current += 1

    def initialize(self):
        self.x = [0, 1]

