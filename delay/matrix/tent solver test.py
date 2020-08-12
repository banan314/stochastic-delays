from numpy.linalg import LinAlgError
import numpy as np
from delay.matrix.TentPath import TentPath
from delay.matrix.TentSolverWithStay import TentSolverWithStay as TentSolver


def printStationaryAndµAsFractions(stationary, mu):
    s = sum(stationary)
    sstat = ['%d/%d' % (x, s) for x in stationary]
    print(', '.join(sstat))
    print('µ = %d/%d' % (mu, s))


solver4 = TentSolver(N=4, tau=1)
assert solver4.fA(-1) == solver4.N / 2
assert solver4.fA(1) == 1
assert solver4.fB(-2) == 0
assert solver4.fB(1) == solver4.N / 2
# print(solver4.statesOfA)
# print(TentPath(2, [-1, 1, 1]).previous())
# print(TentPath(2, [-1, 1, 1]))
# print([str(x) for x in TentPath.generate(-2, 1, edge = True)])
# print([str(x) for x in TentPath.generate(2, 1, edge = True)])
# print([str(x) for x in TentPath.generate(0, 1, edge = False)])
# print([str(x) for x in solver4.generatePaths()])

p = TentPath(-2, [0])
assert p.previous()[0] == -2

solver = TentSolver(N=4, tau=1)

try:
    solver.solve(normalize=True, multiplySolution=False)
    assert len(solver.solution) == len(solver.paths) == len(solver.A)
    # print(solver.solution)
    # print(solver.stationary)
    solver.castToInteger()
    printStationaryAndµAsFractions(solver.stationary, np.rint(solver.calculateMean()).astype(int))
except LinAlgError as e:
    print(e)
# print(solver.A)
# print([str(x) for x in solver.statesOfA])
# print([str(x) for x in solver.paths])
print('µ = ', solver.calculateMean())

print(''.join(solver.printALatex(ampersand=True)))

v = [1, 2]
solver.normalize(v)
assert v == [1 / 3, 2 / 3]

print('success')
