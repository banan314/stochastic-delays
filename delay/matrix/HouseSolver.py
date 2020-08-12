from fractions import Fraction
from typing import List, Any
import numpy as np

from delay.calculator import linear
from delay.matrix.Matrix import Matrix
from delay.matrix.Path import Path
from delay.matrix.Solver import Solver


class HouseSolver(Solver):
    def __init__(self, matrix: Matrix = None, tau=None, d=None):
        self.paths = None
        self.stationary = []
        self.solution = None
        if matrix:
            self.matrix = matrix
            self.tau = matrix.tau
            self.d = matrix.d
        if tau and d:
            self.tau = tau
            self.d = d
            self.matrix = Matrix(tau=tau, d=d)

        self.N = self.numberOfPathsPerState() * (2 * self.tau + 2)
        self.A = np.zeros((self.N, self.N))
        self.probability = linear(N=self.N, w=1.0)

    def generatePaths(self):
        paths = Path.generate(self.d - self.tau, self.tau)
        for i in range(self.d - self.tau + 1, self.d + self.tau + 2):
            paths += Path.generate(i, self.tau)
        return paths

    def solve(self, normalize=True, multiplySolution=False):
        self.paths = self.generatePaths()

        if 2*self.d > self.tau:
            B = self.solveMediumUnbiasedWalk(normalize)
        else:
            B = self.solveShortUnbiasedWalk(normalize)

        print(''.join(self.printALatex()))

        self.solution = np.linalg.solve(self.A, B)
        if multiplySolution:
            self.solution *= multiplySolution
        self.calculateStationary()

    def solveMediumUnbiasedWalk(self, normalize):
        # ignore first `numberOfPaths` because they are on the random walk
        for i in range(self.numberOfPathsPerState(), self.N):
            for j in range(self.N):
                self.A[i, j] = self.matrix.calculateProbability(self.paths[i], self.paths[j])
        self.fillDiagonal()
        B = np.zeros(self.N)
        filler = (1 / 2) ** self.tau if normalize else 1
        for i in range(self.numberOfPathsPerState()):
            B[i] = filler
        return B

    def fillDiagonal(self):
        for i in range(self.numberOfPathsPerState()):
            self.A[i, i] = 1
        for i in range(self.numberOfPathsPerState(), self.N):
            self.A[i, i] -= 1.0

    def numberOfPathsPerState(self):
        return self.N

    def calculateStationary(self):
        self.stationary = []
        for i in range(int(self.N / self.numberOfPathsPerState())):
            s = sum(self.solution[self.numberOfPathsPerState() * i: self.numberOfPathsPerState() * (i + 1)])
            self.stationary.append(s)

    def calculateMean(self):
        sumOfAbs = 1 / 2 + (self.d + 1 + self.d - self.tau - 1)  # obvious ones
        sumOfAbs += sum(self.stationary)  # stationary includes d-tau
        a = 1 / sumOfAbs
        theSum = 1 / 2 * (-(self.d + 1))
        theSum -= sum(range(self.d - self.tau, self.d + 1))
        for i in range(len(self.stationary)):
            index = self.d - self.tau + i
            theSum += index * self.stationary[i]
        return theSum * a

    def numberOfPathsPerState(self):
        return 2 ** self.tau

    def numberOfStates(self):
        return self.N

    def initialLatexLine(self, endl):
        return ['d = %d' % (self.d) + endl]

    def solveShortUnbiasedWalk(self, normalize):
        for i in range(self.currentNumberOfPaths()):
            for j in range(self.currentNumberOfPaths()):
                self.A[i, j] = self.calculateProbability(self.paths[i], self.paths[j])

        self.clearUnreachableStates()

        for i in range(len(self.A)):
            self.A[0, i] = 0

        for i in range(len(self.A)):
            self.A[i, i] -= 1

        B = np.zeros(len(self.A))
        self.A[0, 0] = 1
        B[0] = 1
        return B

    def currentNumberOfPaths(self):
        return len(self.paths)

    def calculateProbability(self, p1: Path, p2: Path):
        if not self.checkAccordance(p1, p2):
            return 0.0
        prob = 1.0
        previousStatesPast = p2.previous()
        previousStatesFuture = p1.previous()

        for i, w in enumerate(p1.path[::-1]):
            w = -w

            p = self.calculateRightProbability(previousStatesPast[i], previousStatesFuture[i])

            if w == 1:
                prob *= p
            else:
                prob *= self.leftProbabilityFromRight(p)
        return prob

    def fA(self, xA):
        if xA <= self.d:
            return self.N/2
        else:
            return 0

    def fB(self, xB):
        if xB < -self.d:
            return 0
        else:
            return self.N/2

    def checkAccordance(self, p1, p2):
        """
        :param p1: future
        :param p2: past
        :return: p1 can be made after p2 or not
        """
        if abs(p1.alpha - p2.alpha) > self.tau:
            return False
        return Path.checkAccordance(p1, p2)

    def numberOfLatexElements(self) -> int:
        return len(self.A)

