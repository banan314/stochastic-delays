import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
print(os.getcwd())
sys.path.append('/home/kamil/Documents/bioinformatyka/grant/simulations')

from delay.regression import linearRegression, Dependence


x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y = [223.12620482989615-250, -26.80846553, -25.42420759, -27.47273278, -24.85779212, -24.26662338, -25.24619746, -24.52194651, -26.3826081, -24.76537977, -24.18099481]


linearRegression(x, y, dependence=Dependence.N, imgFile='tests/img/whatever')
