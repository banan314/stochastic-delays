import numpy as np

from delay.matrix.TentPath import TentPath
from delay.matrix.TentSolver import TentSolver


class TentSolverWithStay(TentSolver):
    @property
    def minimalState(self) -> int:
        return -self.d

    def numberOfStates(self):
        return self.N + 1

    def generatePaths(self):
        v = []
        # -N/2
        v += TentPath.generate(-self.N / 2, self.tau, stay=True, edge=True)

        # middle
        for i in TentSolver.irange(-self.N / 2 + 1, self.N / 2):
            v += TentPath.generate(i, self.tau, stay=False)

        # +N/2
        v += TentPath.generate(self.N / 2, self.tau, stay=True, edge=True)
        return v

    def calculateProbability(self, p1: TentPath, p2: TentPath):
        if not self.checkAccordance(p1, p2):
            return 0.0
        prob = 1.0
        previousStatesPast = p2.previous()
        previousStatesFuture = p1.previous()

        for i, w in enumerate(p1.path[::-1]):
            w = -w

            p = self.calculateRightProbability(previousStatesPast[i], previousStatesFuture[i])

            if w == 1 or (p1.alpha == self.d and w == 0):
                prob *= p
            else:
                prob *= self.leftProbabilityFromRight(p)
        return prob

    def calculateBigN(self):
        return self.numberOfPathsPerState() * self.numberOfStates()

    def stateSpace(self):
        return np.array(np.linspace(int(-self.N / 2), int(self.N / 2), num=self.numberOfStates()))
