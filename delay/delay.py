import matplotlib.pyplot as plt
import random
import numpy as np
import math
from delay.value import calculateValue


class Delay:

    def __init__(self, *args, **kwargs):
        self.duration = 0
        self.tauA = 0
        self.tauB = 0
        self.calculateProbability = None
        self.x = []

    def calculator(self, N, w=0.95):
        def calculate(r):
            return 0.5 + w*(r)/N
        return calculate

    def modelFunctions(self, N, d=20):
        def fA(x):
            return N/4*(math.tanh(-0.6*(x-d))+1)

        def fB(x):
            return N/4*(math.tanh(0.6*(x+d))+1)

        return (fA, fB)

    def simulate(self):
        def nextElem(func):
            term = -N/2 if func == max else N/2
            rc = calculateValue(previousA, previousB)
            value = -rc if func == max else rc
            return func(x[current] + value, term)

        current = len(x)-1
        for _ in range(0, duration):
            previousA, previousB = fA(x[current - tauA]), fB(x[current - tauB])

            prob = calculateProbability(previousA - previousB)
            r = random.random()
            if r <= prob:
                nextElement = nextElem(min)  # +1
            else:
                nextElement = nextElem(max)  # -1

            x.append(nextElement)
            current += 1

