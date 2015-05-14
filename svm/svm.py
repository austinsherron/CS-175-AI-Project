import math
import random

def dot(a, b):
  v = 0
  for i in range(len(a)):
    v += a[i] * b[i]
  return v

def scale(vector, scale):
  new_vector = []
  for i in range(len(vector)):
    new_vector.append(scale * vector[i])
  return new_vector

def add(v1, v2):
  new_vector = []
  for i in range(len(v1)):
    new_vector.append(v1[i] + v2[i])
  return new_vector

def kernel_polynomial(x1, x2, p):
  return dot(x1, x2) ** p

def kernel_rbf(x1, x2, gamma):
  d = []
  for i in range(len(x1)):
    d.append(x1[i] - x2[i])
  return math.exp(-gamma * dot(d, d))

def calc_w(alphas, Y, X):
  w = scale(X[0], alphas[0] * Y[0])
  for i in range(1, len(alphas)):
    w = add(w, scale(X[i], alphas[i] * Y[i]))
  return w

def f(X, Y, kernel, kernelArg, bias, x, alphas):
  v = bias
  for i in range(len(Y)):
    v += alphas[i] * Y[i] * kernel(X[i], x, kernelArg)
  return v

def err(X, Y, x, y, kernel, kernelArg, bias, alphas):
  return f(X, Y, kernel, kernelArg, bias, x, alphas) - y

def rand_select(limit, dont_select):
  r = random.randint(0, limit - 2)
  if r == dont_select:
    return limit - 1
  return r

def get_LH(alpha_i, alpha_j, y_i, y_j, C):
  if y_i == y_j:
    return (max(0, alpha_i + alpha_j - C), min(C, alpha_i + alpha_j))
  return (max(0, alpha_j - alpha_i), min(C, C + alpha_j - alpha_i))


def new_alpha_j(old_alpha, y, Ei, Ej, n, H, L):
  alpha = old_alpha - y * (Ei - Ej) / n
  if alpha > H:
    return H
  if alpha < L:
    return L
  return alpha

def new_alpha_i(old_alpha, yi, yj, old_alpha_j, alpha_j):
  return old_alpha + yi * yj * (old_alpha_j - alpha_j)

def new_bias(bias, E, yi, yj, alpha_i, old_alpha_i, alpha_j, old_alpha_j,
    kernel, kernelArg, xi, xj, firstParam, secondParam):
  return bias - E - yi * (alpha_i - old_alpha_i) * \
      kernel(xi, firstParam, kernelArg) - yj * (alpha_j - old_alpha_j) * \
      kernel(secondParam, xj, kernelArg)

def train_svm_parameters(X, Y, C = 1, kernel = kernel_polynomial,
    kernelArg = 1, max_passes = 10000, tol = 0.001):
  alphas = []
  old_alphas = []
  bias = 0
  passes = 0
  for i in range(len(Y)):
    alphas.append(0)
    old_alphas.append(0)

  while passes < max_passes:
    num_changed_alphas = 0
    for i in range(len(alphas)):
      Ei = err(X, Y, X[i], Y[i], kernel, kernelArg, bias, alphas)
      if Y[i] * Ei < -tol and alphas[i] < C \
          or Y[i] * Ei > tol and alphas[i] > 0:
        j = rand_select(len(alphas), i)
        Ej = err(X, Y, X[j], Y[j], kernel, kernelArg, bias, alphas)
        old_alphas[i] = alphas[i]
        old_alphas[j] = alphas[j]
        L, H = get_LH(alphas[i], alphas[j], Y[i], Y[j], C)
        if L == H:
          continue
        n = 2 * kernel(X[i], X[j], kernelArg) - kernel(X[i], X[i], kernelArg) \
            - kernel(X[j], X[j], kernelArg)
        if n >= 0:
          continue
        alphas[j] = new_alpha_j(alphas[j], Y[j], Ei, Ej, n, H, L)
        if abs(alphas[j] - old_alphas[j]) < 1e-05:
          continue
        alphas[i] = new_alpha_i(alphas[i], Y[i], Y[j], old_alphas[j], \
            alphas[j])
        b1 = new_bias(bias, Ei, Y[i], Y[j], alphas[i], old_alphas[i], \
            alphas[j], old_alphas[j], kernel, kernelArg, \
            X[i], X[j], X[j], X[i])
        b2 = new_bias(bias, Ei, Y[i], Y[j], alphas[i], old_alphas[i], \
            alphas[j], old_alphas[j], kernel, kernelArg, \
            X[i], X[j], X[i], X[j])
        if alphas[i] < C and alphas[i] > 0:
          bias = b1
        elif alphas[j] < C and alphas[j] > 0:
          bias = b2
        else:
          bias = (b1 + b2) / 2
        num_changed_alphas += 1
    if num_changed_alphas == 0:
      passes += 1
    else:
      passes = 0
  return (calc_w(alphas, Y, X), bias)
