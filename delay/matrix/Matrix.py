from delay.matrix.Path import Path


class Matrix:

    def __init__(self, tau, d):
        self.tau = tau
        self.d = d

    def calculateProbability(self, p1: Path, p2: Path):
        if not self.checkAccordance(p1, p2):
            return 0.0
        if p2.alpha == self.d-self.tau:
            return 0.5**self.tau
        prob = 1.0
        previous = p2.previous()
        for i, w in enumerate(p1.path[::-1]):
            w = -w
            if previous[i] <= self.d:
                prob *= 0.5
            else:
                if w == 1:
                    return 0.0
        return prob

    def checkAccordance(self, p1, p2):
        minimum = self.d - self.tau
        if p2.alpha == minimum:
            if p1.alpha + p1.sumPath() < minimum:
                return True
        return Path.checkAccordance(p1, p2)
