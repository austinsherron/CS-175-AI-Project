import math
import numpy as np

class polynomial:
  def __init__(self, p):
    self.p = p
  
  def __call__(self, x1, x2):
    return np.dot(x1, x2) ** self.p

def linear():
  return polynomial(1)

def quadratic():
  return polynomial(2)

class rbf:
  def __init__(self, gamma):
    self.gamma = gamma

  def __call__(self, x1, x2):
    d = np.subtract(x1, x2)
    return math.exp(-self.gamma * np.dot(d, d))
