import sys
sys.path.insert(0, "/home/kamil/Documents/bioinformatyka/grant/simulations")

#!/usr/bin/env python
# coding: utf-8

# In[1]:



# In[2]:


from delay.matrix.Path import *
from delay.matrix.Matrix import *
import numpy as np


# In[3]:


p1 = Path(2, [-1, 1])
p2 = Path(2, [1, 1])
Path.checkAccordance(p1, p2)


# In[4]:


tau = 1
d = 2
n = 2**tau * (2*tau + 2)
A = np.zeros((n, n))
print(n)


# In[5]:


[p.path for p in Path.generate(1, 1)]


# In[6]:


def generatePaths(d, tau):
    paths = Path.generate(d-tau, tau)
    for i in range(d-tau+1, d+tau+2):
        paths += Path.generate(i, tau)
    return paths
v = generatePaths(d, tau)
print([v.alpha for v in v])
print([v.path for v in v])


# In[7]:


m = Matrix(tau=tau, d=d)

for i in range(n):
    for j in range(n):
        A[i, j] = m.calculateProbability(v[i], v[j])

