import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append('/home/kamil/Documents/bioinformatyka/grant/simulations')


import pytest
from delay.simulation import Simulation
from delay.simulation import FunctionType
from delay.value import calculateValue
import delay.calculator as calc

def test_simulation():
    simulation = Simulation(FunctionType.HARD_INTERVAL,                          (20, 0), calculateValue, calc.linear(100))
