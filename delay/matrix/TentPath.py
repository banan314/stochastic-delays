import itertools

from delay.matrix.Path import Path


class TentPath(Path):

    def pathToSigns(self):
        s = ''
        for p in self.path:
            if p == -1:
                s += '+'
            elif p == 1:
                s += '-'
            else:
                s += '0'
        return s[::-1]

    def generate(alpha, tau, stay, edge=False):
        if edge:
            paths = []
            possibleActions = [-1, 0, 1] if stay else [-1, 1]
            combinations = itertools.product(possibleActions, repeat=tau)
            for c in combinations:
                path = TentPath(alpha, list(c))
                previous = path.previous()[0]
                if alpha > 0:
                    if previous <= alpha:
                        paths.append(path)
                elif alpha < 0:
                    if previous >= alpha:
                        paths.append(path)
            return paths
        return Path.generate(alpha, tau)