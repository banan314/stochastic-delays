from fractions import Fraction
import numpy as np

from delay.matrix.Matrix import Matrix
from delay.matrix.Path import Path


class Solver:
    def __init__(self):
        self.solution = None
        self.stationary = None
        self.tau = None
        self.N = None
        self.A = None
        self.paths = None
        self.d = None
        self.probability = None

    def printSolution(self):
        print(self.solution)

    def printStationary(self):
        print(self.stationary)

    def printFractionStationary(self):
        limit = self.fractionLimit()
        print([str(Fraction(p).limit_denominator(limit)) for p in self.stationary])

    def fractionLimit(self):
        return 30 * 2 ** self.tau

    def printALatex(self, ampersand=False, backslash = '\\'):
        def pi(p: Path):
            return backslash + 'pi(%d, %s)' % (p.alpha, p.pathToSigns())

        def toFrac(x):
            if x == 1:
                return ''
            rational = Fraction(x).limit_denominator(30 * self.tau)
            return backslash + 'frac{%d}{%d}' % (rational.numerator, rational.denominator)

        endl = backslash * 2 + '\n'
        equals = ' &= ' if ampersand else ' = '
        plus = ' + '
        lines = self.initialLatexLine(endl)
        threshold = 0.001
        lastLine = ''

        for i in range(self.numberOfLatexElements()):
            components = []
            for j in range(self.numberOfLatexElements()):
                if self.A[i, j] <= threshold:
                    continue
                components.append(toFrac(self.A[i, j]) + pi(self.paths[j]))

            if components:
                line = pi(self.paths[i])
                line += equals
                line += plus.join(components)
                if lastLine:
                    lastLine += endl
                    lines.append(lastLine)
                lastLine = line

        if lastLine:
            lines.append(lastLine)

        # print(''.join(lines))
        return lines

    def initialLatexLine(self, endl: str) -> list:
        pass

    def numberOfPathsPerState(self) -> int:
        pass

    def castToInteger(self):
        self.solution = np.rint(self.solution).astype(int)
        self.stationary = np.rint(self.stationary).astype(int)

    def numberOfPaths(self) -> int:
        pass

    def numberOfStates(self) -> int:
        pass

    def numberOfLatexElements(self) -> int:
        return self.numberOfStates()

    def leftProbabilityFromRight(self, prob):
        return 1 - prob

    def calculateRightProbability(self, xA, xB):
        difference = self.fA(xA) - self.fB(xB)
        prob = self.probability(difference)
        return prob

    def clearUnreachableStates(self):
        aStateRemoved = True
        while aStateRemoved:
            aStateRemoved = False
            for i in range(len(self.A)):
                isUnreachable = True
                for j in range(len(self.A)):
                    if i != j:
                        if self.A[i, j] != 0:
                            isUnreachable = False
                if isUnreachable:
                    self.deleteAState(i)
                    aStateRemoved = True
                    break

    def deleteAState(self, state):
        self.A = np.delete(self.A, state, 0)
        self.A = np.delete(self.A, state, 1)
        self.paths.__delitem__(state)

    def fA(self, xA: int) -> int:
        pass

    def fB(self, xB: int) -> int:
        pass