import kernel
import math
import random
import numpy as np

class Classifier:
  def __evaluate(self, X, Y, x):
    v = self.bias
    for i in range(self.num_samples):
      v += self.alphas[i] * Y[i] * self.kernel(X[i], x)
    return v

  def __err(self, X, Y, ind):
    if ind in self.error_cache:
      return self.error_cache[ind]
    return self.__evaluate(X, Y, X[ind]) - Y[ind]    

  def __rselect(self, limit, dont_select):
    r = random.randint(0, limit - 2)
    if r == dont_select:
      return limit - 1
    return r

  def __bounds(self, Y, C, i, j):
    if Y[i] == Y[j]:
      return max(0, self.alphas[i] + self.alphas[j] - C), \
          min(C, self.alphas[i] + self.alphas[j])
    return max(0, self.alphas[j] - self.alphas[i]), \
        min(C, C + self.alphas[j] - self.alphas[i])

  def __calc_w(self, X, Y):
    self.w = np.zeros(len(X[0]))
    for i in range(self.num_samples):
      self.w = np.add(self.w, np.multiply(X[i], self.alphas[i] * Y[i]))

  def __new_alpha_j(self, Y, j, Ei, Ej, n, H, L):
    alpha = self.alphas[j] + Y[j] * (Ei - Ej) / n
    if alpha > H:
      return H
    if alpha < L:
      return L
    return alpha

  def __new_alpha_i(self, Y, i, j):
    return self.alphas[i] + Y[i] * Y[j] * (self.old_alphas[j] - self.alphas[j])

  def __new_bias(self, E, X, Y, i, j, param):
    return self.bias - E - Y[i] * (self.alphas[i] - self.old_alphas[i]) \
      * self.kernel(X[i], X[param]) \
      - Y[j] * (self.alphas[j] - self.old_alphas[j]) \
      * self.kernel(X[param], X[j])

  def __remap_labels(self, Y):
    labels = np.zeros(len(Y))
    first_label = Y[0]
    second_label = None
    for i in range(len(Y)):
      if Y[i] == first_label:
        labels[i] = 1
      else:
        second_label = Y[i]
        labels[i] = -1
    return labels, first_label, second_label
  
  def predict(self, x):
    v = self.kernel(x, self.w) + self.bias
    if v >= 0:
      return self.pos
    else:
      return self.neg

  def __update_error_cache(self, X, Y, C):
    self.error_cache = {}
    for i in self.__non_zeroC_alpha(C):
      self.error_cache[i] = self.__err(X, Y, i)

  def __take_step(self, X, Y, Ej, i, j, C, tol):
    if i == j:
      return False
    Ei = self.__err(X, Y, i)
    L, H = self.__bounds(Y, C, i, j)
    if L == H:
      return False
    self.old_alphas[i] = self.alphas[i]
    self.old_alphas[j] = self.alphas[j]
    n = -2 * self.kernel(X[i], X[j]) + self.kernel(X[i], X[i]) \
        + self.kernel(X[j], X[j])
    if n < 0:
      return False
    self.alphas[j] = self.__new_alpha_j(Y, j, Ei, Ej, n, H, L)
    if abs(self.alphas[j] - self.old_alphas[j]) < tol:
      return False
    if self.alphas[j] < tol:
      self.alphas[j] = 0
    elif self.alphas[j] > C - tol:
      self.alphas[j] = C
    self.alphas[i] = self.__new_alpha_i(Y, i, j)
    b1 = self.__new_bias(Ei, X, Y, i, j, i)
    b2 = self.__new_bias(Ej, X, Y, i, j, j)
    if self.alphas[i] < C and self.alphas[i] > 0:
      self.bias = b1
    elif self.alphas[j] < C and self.alphas[j] > 0:
      self.bias = b2
    else:
      self.bias = (b1 + b2) / 2
    self.__update_error_cache(X, Y, C)
    return True

  def __non_zeroC_alpha(self, C):
    arr = []
    for i in range(len(self.alphas)):
      alpha = self.alphas[i]
      if not alpha == 0 and not alpha == C:
        arr.append(i)
    return arr

  def __shuffle(self, arr):
    for i in range(len(arr)):
      ind = random.randint(i, len(arr) - 1)
      temp = arr[i]
      arr[i] = arr[ind]
      arr[ind] = temp
    return arr

  def __second_heuristic(self, non_optimal, Ej, X, Y):
    best = None
    bestE = None
    for i in non_optimal:
      Ei = self.__err(X, Y, i)
      if best == None or abs(Ej - Ei) > bestE:
        best = i
        bestE = abs(Ej - Ei)
    return best

  def __examine_example(self, X, Y, j, C, tol):
    Ej = self.__err(X, Y, j)
    r = Ej * Y[j]
    if r < -tol and self.alphas[j] < C or r > tol and self.alphas[j] > 0:
      non_optimal = self.__non_zeroC_alpha(C)
      if len(non_optimal) > 1:
        i = self.__second_heuristic(non_optimal, Ej, X, Y)
        if self.__take_step(X, Y, Ej, int(i), int(j), C, tol):
          return True

      for i in self.__shuffle(self.__non_zeroC_alpha(C)):
        if self.__take_step(X, Y, Ej, int(i), int(j), C, tol):
          return True
  
      for i in self.__shuffle(self.alphas):
        if self.__take_step(X, Y, Ej, int(i), int(j), C, tol):
          return True
    return False

  def train(self, X, Y, C, kernel, tol):
    self.num_samples = len(Y)
    self.kernel = kernel
    self.alphas = np.zeros(self.num_samples)
    self.old_alphas = np.zeros(self.num_samples)
    self.bias = 0
    self.error_cache = {}
    num_changed = 0
    examine_all = True
    while num_changed > 0 or examine_all:
      num_changed = 0
      if examine_all:
        for j in range(len(X)):
          if self.__examine_example(X, Y, j, C, tol):
            num_changed += 1
      else:
        for j in self.__non_zeroC_alpha(C):
          if self.__examine_example(X, Y, j, C, tol):
            num_changed += 1
      if examine_all:
        examine_all = False
      elif num_changed == 0:
        examine_all = True
    self.__calc_w(X, Y)

  def __init__(self, X, Y, C = 1, kernel = kernel.linear(), tol = 1e-3):
    Y, self.pos, self.neg = self.__remap_labels(Y)
    self.train(X, Y, C, kernel, tol)
