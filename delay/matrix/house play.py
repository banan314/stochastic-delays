from sympy import symbols, simplify

from delay.matrix.HouseSolver import HouseSolver
from delay.matrix.Matrix import Matrix as DelayMatrix

m = DelayMatrix(tau=2, d=0)
solver = HouseSolver(matrix=m)

solver.solve(normalize=False, multiplySolution=6)
# solver.castToInteger()

solver.printFractionStationary()
# print(''.join(solver.printALatex(ampersand=True, backslash='\\')))

print(solver.calculateMean())

# solver.printStationary()

# d = symbols('d')
# a = 1/2 + 2*d - solver.tau + 1
# for s in solver.stationary[1:]:
#     a += s / solver.stationary[0]
# a = 1/a
# print(simplify(a))
# mu = -(d+1)/2
# for t in range(solver.tau):
#     print(-d + t)
#     mu += (-d + t)
# for x in range(-solver.tau+1, solver.tau+2):
#     print((d + x)*solver.stationary[x + solver.tau]/solver.stationary[0])
#     mu += (d + x)*solver.stationary[x + solver.tau]/solver.stationary[0]
# mu *= a
# print(simplify(mu))
