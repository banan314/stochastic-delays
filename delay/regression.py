import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from enum import Enum

# Create linear regression object
regr = linear_model.LinearRegression()


class Dependence(Enum):
    D = 0
    TAU = 1
    N = 2


def whereGreater(x, threshold):
    t = 0
    for i in range(0, len(x)):
        while(x[t] <= threshold):
            t += 1
    return slice(t, len(x))


def whereGreaterOrEqual(x, threshold):
    t = 0
    for i in range(0, len(x)):
        while(x[t] < threshold):
            t += 1
    return slice(t, len(x))


def whereInside(x, bottom, top):
    """
    from the interval [b, t)
    """
    b = 0
    t = 0
    while(x[b] < bottom):
        b += 1
    t = b
    while(x[t] < top):
        if len(x) > t+1:
            t += 1
        else:
            break
    return slice(b, t)


def whereSmaller(x, threshold):
    t = 0
    while(x[t] < threshold):
        if len(x) > t+1:
            t += 1
        else:
            break
    return slice(0, t)


def whereSmallerOrEqual(x, threshold):
    t = 0
    while(x[t] <= threshold):
        if len(x) > t+1:
            t += 1
        else:
            break
    return slice(0, t)


def linearRegression(x, y, dependence, imgFile=None, smallerThan=None, showFit=True, forHalfN=False, N=0, error=None, showOnlyPointsSmallerThanHalf=False):

    def variable(dependence):
        if dependence == Dependence.D:
            return 'd'
        if dependence == Dependence.TAU:
            return 'τ'
        return 'N'

    x = np.array(x).reshape(-1, 1)

    # Train the model using the training sets
    if smallerThan:
        smaller = whereSmallerOrEqual(x, smallerThan)
        xInterest = x[smaller]
        yInterest = y[smaller]
    elif forHalfN:
        v = N/2 if dependence == Dependence.TAU else N/2-8
        smaller = whereSmallerOrEqual(x, v)
        xInterest = x[smaller]
        yInterest = y[smaller]
    else:
        xInterest = x
        yInterest = y
    regr.fit(xInterest, yInterest)

    # Make predictions using the testing set
    y_pred = regr.predict(xInterest)

    plt.figure(figsize=(8, 6))

    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(yInterest, y_pred))
    # Explained variance score: 1 is perfect prediction
    print('Variance score (R^2): %.2f' % r2_score(yInterest, y_pred))

    # Plot outputs
    if showOnlyPointsSmallerThanHalf:
        takeSlice = whereSmaller(x, N/2)
        plt.scatter(x[takeSlice], y[takeSlice], color='black')
    else:
        plt.scatter(x, y,  color='black')

    if error:
        plt.errorbar(x, y, yerr=error)
    if showFit:
        plt.plot(xInterest, y_pred, color='blue', linewidth=3)

    intercept = regr.intercept_

    print('Line: ' + '%.2f%s + %f' % (regr.coef_, variable(dependence), intercept))

    plt.ylabel(r'$\mu$', usetex=True, fontsize=30, labelpad=0.0)
    plt.xlabel(dependenceToTex(dependence), usetex=True, fontsize=30)

    if imgFile:
        plt.savefig(imgFile)

    plt.show()
    return {'max': max(xInterest).tolist()[0], 'r2': r2_score(yInterest, y_pred), 'mse': mean_squared_error(yInterest, y_pred), 'slope': regr.coef_, 'intercept': intercept,
        'var': variable(dependence), 'upto': smallerThan if smallerThan else max(x)}


def dependenceToTex(dependence):
    if dependence == Dependence.D:
        return r'$d$'
    elif dependence == Dependence.N:
        return r'$N$'
    elif dependence == Dependence.TAU:
        return r'$\tau_A$'

