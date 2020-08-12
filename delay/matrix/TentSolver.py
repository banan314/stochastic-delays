from delay.calculator import linear
from delay.matrix.Path import Path
from delay.matrix.Solver import Solver
from delay.matrix.TentPath import TentPath
import numpy as np


class TentSolver(Solver):

    def __init__(self, N, tau):
        self.tau = tau
        self.N = N  # number of states - 1
        self.d = int(self.N / 2)
        self.penultimateParity = (self.minimalState+1) % 2

        self.probability = linear(N=self.N, w=1.0)

        self.A = None

    @property
    def minimalState(self) -> int:
        pass

    def calculateBigN(self):
        """
        calculate the widht/height of matrix A, used in solve method
        :return: bigN --- total number of paths
        """
        pass

    def irange(a, b):
        return range(int(a), int(b))

    def numberOfStates(self) -> int:
        pass

    def solve(self, normalize=True, multiplySolution=False):
        if self.tau % 2:
            self.solve_odd(normalize, multiplySolution)
        else:
            self.solve_even(normalize, multiplySolution)

    def solve_odd(self, normalize=True, multiplySolution=False):
        self._solve1()
        self.clearRows([0])
        self.fillDiagonal()
        B = self.set1InRow([0])
        self._solve2(multiplySolution, normalize, B)

    def solve_even(self, normalize=True, multiplySolution=False):
        self._solve1()
        rowOf1 = self.firstRowOfPenultimate()
        self.clearRows([0, rowOf1])
        self.fillDiagonal()
        B = self.set1InRow([0, rowOf1])
        self._solve2(multiplySolution, normalize, B)

    def _solve1(self):
        self.paths = self.generatePaths()
        self.A = np.zeros((self.currentNumberOfPaths(), self.currentNumberOfPaths()))

        for i in range(self.currentNumberOfPaths()):
            for j in range(self.currentNumberOfPaths()):
                self.A[i, j] = self.calculateProbability(self.paths[i], self.paths[j])

        self.clearUnreachableStates()

    def set1InRow(self, rows):
        B = np.zeros(len(self.A))
        for r in rows:
            self.A[r, r] = 1
            B[r] = 1
        return B

    def _solve2(self, multiplySolution, normalize, B):
        self.solution = np.linalg.solve(self.A, B)

        if self.tau % 2 == 0:
            self.multiplyOddStates(self.calculateEvenOddRatio())
        if normalize:
            self.normalize(self.solution)
        if multiplySolution:
            self.solution *= multiplySolution
        self.calculateStationary()

    def fillDiagonal(self):
        for i in range(len(self.A)):
            self.A[i, i] -= 1

    def fA(self, x):
        return self.d if x <= 0 else max(self.d - x, 0)

    def fB(self, x):
        return max(self.d + x, 0) if x <= 0 else self.d

    def calculateStationary(self):
        self.stationary = np.zeros(self.numberOfStates())
        for i in range(self.currentNumberOfPaths()):
            id = int(self.paths[i].alpha - self.minimalState)
            self.stationary[id] += self.solution[i]

    def currentNumberOfPaths(self):
        return len(self.paths)

    def calculateProbability(self, p1: TentPath, p2: TentPath):
        """
        :param p1: future
        :param p2: past
        :return: probability of the path p1 provided that alpha was reached by p2
        """
        pass

    def checkAccordance(self, p1, p2):
        """
        :param p1: future
        :param p2: past
        :return: p1 can be made after p2 or not
        """
        if abs(p1.alpha - p2.alpha) > self.tau:
            return False
        return TentPath.checkAccordance(p1, p2)

    def generatePaths(self):
        pass

    def numberOfPathsPerState(self):
        """
        :return: number of paths per state
        """
        return int(2 ** self.tau)

    def clearRows(self, rows):
        for r in rows:
            for i in range(len(self.A)):
                self.A[r, i] = 0

    def calculateMean(self):
        return np.dot(self.stationary, self.stateSpace())

    def stateSpace(self) -> list:
        pass

    def normalize(self, vector):
        s = sum(vector)
        for i in range(len(vector)):
            vector[i] /= s

    def fractionLimit(self):
        return super().fractionLimit() * self.N

    def initialLatexLine(self, endl):
        return []

    def numberOfLatexElements(self) -> int:
        return self.currentNumberOfPaths()

    def numberOfPathProbabilities(self):
        """
        :return: total number of paths
        """
        return len(self.A)

    def multiplyOddStates(self, c):
        for i in range(len(self.solution)):
            if self.paths[i].alpha % 2 == self.penultimateParity:
                self.solution[i] *= c

    def calculateEvenOddRatio(self):
        penultimateSum = 0.0
        ultimateStationary = 0.0
        for i in range(len(self.solution)):
            if self.paths[i].alpha == self.minimalState:
                ultimateStationary += self.solution[i]
            if self.paths[i].alpha == self.minimalState + 1:
                path = self.paths[i]
                prob = self.calculateRightProbability(path.previous()[0], path.alpha)
                prob = self.leftProbabilityFromRight(prob)
                penultimateSum += prob * self.solution[i]
        return ultimateStationary / penultimateSum

    def firstRowOfPenultimate(self):
        for i in range(len(self.paths)):
            if self.paths[i].alpha == self.minimalState + 1:
                return i
