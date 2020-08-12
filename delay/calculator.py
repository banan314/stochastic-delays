import numpy as np
import matplotlib.pyplot as plt
import math


def linear(N, w=0.95):
    def calculate(r):
        return 0.5 + w*(r)/N
    return calculate


def exponential(N, beta=1):
    def calculate(fa, fb):
        return math.exp(beta*fa)/(math.exp(beta*fa) + math.exp(beta*fb))
    return calculate


def bezier(n=100):
    t = np.linspace(0, 1, num=100000)
    xt = (3*(1-t)*t*t+t*t*t)*200-100
    yt = 3*(1-t)*(1-t)*t+t*t*t
    lut = {}
    j = 0
    epsilon = 0.01
    for i in range(-n, n+1):
        while(abs(xt[j] - i) > epsilon):
            j += 1
        lut[i] = yt[j]

    def calculate(r):
        return lut[r]
    return calculate


def step(d=20, epsilon=0.01):
    def calculate(r):
        if r < -d:
            return epsilon
        if -d <= r <= d:
            return 0.5
        if d < r:
            return 1-epsilon
    return calculate


def stepWithoutInterval(N, w=0.95):
    def calculate(r):
        if r < 0:
            return 1-w
        if r == 0:
            return 0.5
        return w
    return calculate


def parametric(pd=0.05, s=10, d=20, epsilon=0.01):
    def calculate(r):
        if r <= -(s + d):
            return epsilon
        if -(s+d) < r <= -d:
            return (0.5 - pd)/s*r + (0.5-pd)/s*(s+d)
        if -d < r <= d:
            return 0.5 + pd/d*r
        if d < r <= d+s:
            return ((1-0.5-pd)/s) * (r - s - d) + 1
        if d+s < r:
            return 1-epsilon
    return calculate


def unbiased(pd=0.05, s=10, d=20, epsilon=0.01):
    def calculate(r):
        if r <= -(s + d):
            return epsilon
        if -(s+d) < r <= -d:
            return (0.5 - pd)/s*r + (0.5-pd)/s*(s+d)
        if -d < r < d:
            return 0.5 + pd/d*r
        if d <= r < d+s:
            return ((1-0.5-pd)/s) * (r - s - d) + 1
        if d+s <= r:
            return 1-epsilon
    return calculate


def smooth(d, w=0.95):
    def calculate(r):
        return 1/4*(math.tanh(r-d) + math.tanh(r+d)) + 1/2
    return calculate


def plot(func):
    N = 100
    x = np.linspace(-N/2, N/2, num=1000)

    y = []
    for xx in x:
        y.append(func(xx))

    plt.plot(x, y, label='p(+1)')

    plt.legend()
    plt.show()
