from delay.matrix.Matrix import Matrix
from delay.matrix.Solver import HouseSolver

m = Matrix(tau=2, d=10)
solver = HouseSolver(matrix=m)
solver.solve()
solver.printFractionStationary()