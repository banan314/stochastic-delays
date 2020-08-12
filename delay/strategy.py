import matplotlib.pyplot as plt
import numpy as np
import math


def fA_TentWithStay(N):
    def compute(x):
        return N / 2 if x <= 0 else N / 2 - x

    return compute


def fB_TentWithStay(N):
    def compute(x):
        return x + N / 2 if x <= 0 else N / 2

    return compute


def fA_TentWithoutStay(N, d):
    def compute(x):
        if x <= 0:
            return d
        if x <= d:
            return d-x
        return 0

    return compute


def fB_TentWithoutStay(N, d):
    def compute(x):
        if x < -d:
            return 0
        if x < 0:
            return x + d
        return d

    return compute


def fA_Hard(N):
    def compute(x):
        return N / 2 if -N / 2 <= x <= 0 else N / 2 - x

    return compute


def fB_Hard(N):
    def compute(x):
        return x + N / 2 if -N / 2 <= x <= 0 else N / 2

    return compute


def fA_Skew45deg(N, d):
    def compute(x):
        k = (N - 2 * d) / 2
        return k if x <= d else -x + k + d

    return compute


def fB_Skew45deg(N, d):
    def compute(x):
        k = (N - 2 * d) / 2
        return k if x >= -d else x + k + d

    return compute


def fA_HardSkew(N, d):
    def compute(x):
        return N / 2 if x <= d else N / 2 - x + d

    return compute


def fB_HardSkew(N, d):
    def compute(x):
        return N / 2 if x >= -d else N / 2 + x + d

    return compute


def fA_HardSkewTo0(N, d):
    def compute(x):
        return N / 2 if x <= d else (-N / 2 * x + (N / 2) * (N / 2)) / (N / 2 - d)

    return compute


def fB_HardSkewTo0(N, d):
    def compute(x):
        return N / 2 if x >= -d else (N / 2 * x + (N / 2) * (N / 2)) / (N / 2 - d)

    return compute


def fA_HardInterval(N, d=20):
    def compute(x):
        return N / 2 if x <= d else 0

    return compute


def fB_HardInterval(N, d=20):
    def compute(x):
        return N / 2 if x >= -d else 0

    return compute


def fA_Smooth(N, d, omega):
    def compute(x):
        return N / 4 * (math.tanh(-omega * (x - d)) + 1)

    return compute


def fB_Smooth(N, d, omega):
    def compute(x):
        return N / 4 * (math.tanh(omega * (x + d)) + 1)

    return compute


def showSmoothFunctions(fA, fB, N, d=20, omega=10, filename=None):
    fA = fA(N, d, omega)
    fB = fB(N, d, omega)

    vfA = np.vectorize(fA)
    vfB = np.vectorize(fB)
    x = np.linspace(-N / 2, N / 2, num=N + 1)

    yA = vfA(x)
    yB = vfB(x)

    plotFunctions(x, yA, yB, filename)


def showNormalFunctions(fA, fB, N, filename=None):
    fA = fA(N)
    fB = fB(N)

    vfA = np.vectorize(fA)
    vfB = np.vectorize(fB)
    x = np.linspace(-N / 2, N / 2, num=N + 1)

    yA = vfA(x)
    yB = vfB(x)

    plotFunctions(x, yA, yB, filename)


def showIntervalFunctions(fA, fB, N, d=20, filename=None):
    fA = fA(N, d)
    fB = fB(N, d)

    vfA = np.vectorize(fA)
    vfB = np.vectorize(fB)
    x = np.linspace(-N / 2, N / 2, num=N + 1)

    yA = vfA(x)
    yB = vfB(x)

    plotFunctions(x, yA, yB, filename)


def plotFunctions(x, yA, yB, filename=None):
    plt.plot(x, yA, label=r'$f_A(x)$')
    plt.plot(x, yB, label=r'$f_B(x)$')
    plt.rc('text', usetex=True)
    plt.rcParams.update({'font.size': 20})

    plt.legend()
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
