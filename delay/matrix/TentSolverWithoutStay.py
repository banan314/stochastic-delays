import numpy as np

from delay.matrix.TentPath import TentPath
from delay.matrix.TentSolver import TentSolver


class TentSolverWithoutStay(TentSolver):

    @property
    def minimalState(self):
        return int(min(-self.d, -self.tau))

    def numberOfStates(self):
        return max(0, self.tau - self.d) + self.N + self.tau + 1

    def generatePaths(self):
        v = []
        # left edge
        for s in range(self.minimalState, -self.d + 1):
            v += TentPath.generate(s, self.tau, stay=False, edge=True)

        # middle
        for i in TentSolver.irange(-self.d + 1, self.d + 1):
            v += TentPath.generate(i, self.tau, stay=False)

        # right edge
        for i in TentSolver.irange(self.d + 1, self.d + self.tau + 1):
            v += TentPath.generate(i, self.tau, stay=False, edge=True)
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

            if w == 1:
                prob *= p
            else:
                prob *= self.leftProbabilityFromRight(p)
        return prob

    def calculateBigN(self):
        return self.numberOfPathsPerState() * (self.numberOfStates() - 1)

    def stateSpace(self):
        return np.array(np.linspace(self.minimalState, int(self.d + self.tau), num=self.numberOfStates()))
