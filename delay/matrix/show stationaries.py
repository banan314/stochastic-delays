from delay.matrix.TentSolverWithoutStay import TentSolverWithoutStay as TentSolver
import numpy as np
import matplotlib.pyplot as plt

def printStationaryAsFractions(stationary):
    s = sum(stationary)
    sstat = ['%d/%d' % (x, s) for x in stationary]
    print(', '.join(sstat))


def printQuotientOfTwo(stationary, last=0):
    if last + 2 > len(stationary):
        print("---")
        return
    if last > 0:
        sstat = [x for x in stationary[-2 - last:-2 - last + 2]]
    else:
        sstat = [x for x in stationary[-2 - last:]]

    print(sstat[0] / sstat[1])


def print0Solutions(solver):
    i = int(solver.N - 1)
    print("N=%d,   %s/%s" % (solver.N, solver.paths[i], solver.paths[i + 1]), end=' = ')
    print(solver.solution[i] / solver.solution[i + 1])


def printMinusSolutions(solver):
    for i in range(0, 2 * solver.N, 2):
        print("%.2f" % solver.solution[i], end=', ')
    print('')


def printMinusSolutionsNeighborQuotients(solver):
    for i in range(0, 2 * solver.N, 2):
        print("%.2f" % (solver.solution[i] / solver.solution[i + 2]), end=', ')
    print('')


def printMinusSolutionsNeighborQuotientsB10(solver):
    i = solver.N + 2
    if i+2 > solver.N * 2:
        return
    print("%s / %s = %.2f, N = %d" % (solver.paths[i], solver.paths[i + 2], solver.solution[i] / solver.solution[i + 2], solver.N))


def checkLeftMinusSolutionsFormula(solver):
    for i in range(0, int(2 * solver.N/2 - 4), 2):
        a0 = solver.solution[i]
        a1 = solver.solution[i + 2]
        a2 = solver.solution[i + 4]
        s = i / 2 + 2
        f = (solver.N - s + 1) / s * a0 +(solver.N - 2*s + 1) / s * a1
        print("%.3f=%.3f" % (f, a2), end=', ')
    print('')


def checkRightMinusSolutionsFormula(solver):
    for i in range(0, int(2 * solver.N/2 - 4), 2):
        offset = solver.N + 2
        a0 = solver.solution[offset + i]
        a1 = solver.solution[offset + i + 2]
        a2 = solver.solution[offset + i + 4]
        s = i / 2 + 2
        f = (solver.N - 2 * s + 2) / (solver.N + 2 * s + 4) * a0 + (-4*s - 2)/(solver.N + 2*s + 4) * a1
        print("%.3f=%.3f" % (f, a2), end=', ')
    print('')

def printAllSensibleSolutionNeighborQuotients(s):
    for i in range(s.N * 2, s.N, -2):
        v = s.solution[i] + s.solution[i - 1]  # pi(v)
        vm = s.solution[i]  # pi(v, -)
        print("%.2f" % (v / vm), end=', ')
    print('')


def printAllStationaryNeighborQuotients(s):
    for i in range(len(s.stationary) - 2):
        print("%.2f" % (s.stationary[i] / s.stationary[i + 1]), end=', ')
    print('')

# solver = TentSolver(N = 6, tau=2)
# solver.solve()
# solver.printFractionStationary()
# solver.stationary

# solvers = []
# for i in range(10):
#     solvers.append(TentSolver(N=i * 2 + 2, tau=2))
# s = TentSolver(N = 10, tau=1)

# for s in solvers:
    # s.solve(normalize=True)
# s.solve(normalize=True)
# s.castToInteger()

    # k = len(s.stationary)
    # z = 1
    # if k-z-3 < 0:
    #     continue
    # print(s.stationary[k-z-3] / s.stationary[k-z-2], "; N=%d" % s.N) # m-z-1/m-z

    # k = len(s.solution)
    # print(s.solution[k-4] / s.solution[k-3])

    # printMinusSolutionsNeighborQuotientsB10(s)

    # checkLeftMinusSolutionsFormula(s)
    # checkRightMinusSolutionsFormula(s)

# s.printStationary()

# print(''.join(s.printALatex(ampersand=True)))
# print('%d/%d' % (s.calculateMean(), sum(s.stationary)))
# print(s.calculateMean())

    # printAllSensibleSolutionNeighborQuotients(s)
    # printAllStationaryNeighborQuotients(s)

    # print0Solutions(s)

    # printStationaryAsFractions(s.stationary)
    # printQuotientOfTwo(s.stationary, last=5)

# taus = [0]
# mus = [0]


taus = np.load('tent-without-d=6-taus.npy')
mus = np.load('tent-without-d=6-mus.npy')

for t in range(7, 9):
    taus = np.append(taus, t)
    s = TentSolver(N = 12, tau=t)
    s.solve(normalize=True)
    mus = np.append(mus, s.calculateMean())
    print('tau = %d' % t)

np.save('tent-without-d=6-taus', taus)
np.save('tent-without-d=6-mus', mus)

f = len(mus)
plt.xticks(np.arange(0, 10, step=1))
plt.xlabel('$\\tau$', usetex=True, fontsize=24)
plt.ylabel('µ', fontsize=24)
plt.title('$\mu(\\tau)$ for $d\'= 6$', usetex = True, fontsize = 25)
plt.plot(taus[0:f], mus[0:f], linestyle='--', marker='o')
plt.savefig('../../../draft/img/tent-without/mu_of_taus-d10-analytical')
plt.show();