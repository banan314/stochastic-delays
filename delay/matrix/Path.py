import itertools

class Path:

    def __init__(self, alpha, path):
        self.alpha = alpha
        self.path = path

    def pathToSigns(self):
        s = ''
        for p in self.path:
            if p == -1:
                s += '+'
            elif p == 1:
                s += '-'
        return s[::-1]

    def sumPath(self):
        return sum(self.path)

    def previous(self):
        current = self.alpha
        previous = []
        for i in range(len(self.path)):
            current += self.path[i]
            previous.append(current)
        return previous[::-1]

    def next(self):
        current = self.alpha
        next = []
        for i in range(len(self.path)):
            current += self.path[i]
            next.append(current)
        return next

    def checkAccordance(p1, p2):
        """
        p1 - Path object, future
        p2 - Path object, past
        """
        return p1.alpha + p1.sumPath() == p2.alpha

    def generate(alpha, tau):
        return [Path(alpha, list(p)) for p in itertools.product([-1, 1], repeat=tau)]

    def __str__(self):
        return 'π(%d, %s)' % (self.alpha, self.pathToSigns())