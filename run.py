import csv
import sys
import random
import math
import pickle

from numpy import zeros
from numpy import transpose
from numpy import matrix
from scipy.linalg import svd
from scipy.sparse.linalg import svds

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

feature_words = dict()
feature_arr = []
documents = []
labels = []
stop_words = dict()

length = 5000

with open(sys.argv[1], 'r') as f:
  for line in f:
    stop_words[line.strip()] = 1
print 'FINISHED STOP WORDS'

with open(sys.argv[2], 'r') as f:
  reader = csv.reader(f, delimiter=',', quotechar='"')
  i = 0
  for row in reader:
    doc = dict()
    words = row[0].split()
    v = float(row[1])
    if v < .1 and v > -.1:
      continue
    for word in words:
      if word in stop_words:
        continue
      if word in feature_words:
        feature_words[word] += 1
      else:
        feature_words[word] = 1
        feature_arr.append(word)
      if word in doc:
        doc[word] += 1
      else:
        doc[word] = 1
    documents.append(doc)
    labels.append(row[2])
    if i > length:
      break
    i += 1
print 'FINISHED DOC PARSING'
global_terms = zeros(len(feature_arr))
for i in range(len(feature_arr)):
  term = feature_arr[i]
  g = 1
  print str(i) + '/' + str(len(feature_arr))
  for j in range(len(documents)):
    doc = documents[j]
    if term in doc and not doc[term] == 0:
      p = float(doc[term]) / float(feature_words[term])
      g += p * math.log(p, 2) / math.log(len(documents), 2)
  global_terms[i] = g

print 'CALCING A'
A = zeros([len(feature_arr), len(documents)])
for i in range(len(feature_arr)):
  print str(i) + '/' + str(len(feature_arr))
  for j in range(len(documents)):
    term = feature_arr[i]
    document = documents[j]
    tf = 0
    if term in document:
      tf = document[term]
    A[i, j] = math.log(1 + tf, 2) * global_terms[i]
print 'SVD'

K = 10
U, S, Vt = svds(transpose(A), k=K)

T = transpose(Vt)

transform = matrix(T)
print 'SVD done'
data = []
for i in range(len(documents)):
  doc = documents[i]
  log_entropy = []
  for j in range(len(feature_arr)):
    word = feature_arr[j]
    if word in doc:
      log_entropy.append(global_terms[j] * math.log(1 + doc[word], 2))
    else:
      log_entropy.append(0)
  transformed_vec = (matrix(log_entropy) * transform).getA()
  feature_vec = []
  for d in transformed_vec.flat:
    feature_vec.append(d)
  data.append([feature_vec, labels[i]])

with open('lsi.pickle', 'w') as f:
  pickle.dump([T, global_terms, feature_arr, data], f)
with open('lsi.pickle', 'r') as f:
  T, global_terms, feature_arr, data = pickle.load(f)
'''
x = []
y = []
z = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
label_color = []
for i in range(len(data)):
  x.append(data[i][0][0])
  y.append(data[i][0][1])
  z.append(data[i][0][2])
  if data[i][1] == '1':
    label_color.append('r')
  else:
    label_color.append('b')
ax.scatter(x, y, z, c=label_color)
plt.show()
'''
'''
feature_words = {}
feature_arr = []
def words_to_feature_vector(words):
  global feature_words
  vector = dict()
  vector_arr = []
  for (key, value) in feature_words.iteritems():
    vector[key] = 0
  for word in words:
    if word in feature_words:
      feature_words[word] += 1
      vector[word] += 1
  for word in feature_arr:
    vector_arr.append(vector[word])
  return vector_arr

with open(sys.argv[1], 'r') as f:
  for line in f:
    feature_words[line.strip()] = 0
    feature_arr.append(line.strip())
'''
'''
data = []
with open(sys.argv[2], 'r') as f:
  reader = csv.reader(f, delimiter=',', quotechar='"')
  i = 0
  for row in reader:
    vector = words_to_feature_vector(row[0].split(' '))
    label = row[2]
    data.append((vector, label))
    if i > length:
      break
    i += 1

for i in range(len(data)):
  for j in range(len(feature_arr)):
    word = feature_arr[j]
    if feature_words[word] != 0:
      data[i][0][j] /= float(feature_words[word])
with open('lsi.pickle', 'r') as f:
  [T, g, feature_arr, data] = pickle.load(f)
'''
random.shuffle(data)
train_count = int(math.floor(len(data) * .7))
test_count = int(math.floor(len(data) * .3))

train_x = []
train_y = []
test_x = []
test_y = []
for i in range(train_count):
  train_x.append(data[i][0])
  train_y.append(data[i][1])

for i in range(test_count):
  test_x.append(data[train_count + i][0])
  test_y.append(data[train_count + i][1])
print 'Training on ' + str(train_count) + ' data points'
'''
classifier = SVC(C=100, gamma=1e-1)
classifier.fit(train_x, train_y)

train_predictions = classifier.predict(train_x)
test_predictions = classifier.predict(test_x)
isPositive = 0
right_train = 0
for k in range(len(train_predictions)):
  if train_predictions[k] == train_y[k]:
    right_train += 1
  if train_y[k] == '1':
    isPositive += 1
print(float(right_train) / len(train_predictions))

right_test = 0
for k in range(len(test_predictions)):
  if test_predictions[k] == test_y[k]:
    right_test += 1
  if test_y[k] == '1':
    isPositive += 1
print(float(right_test) / len(test_predictions))
print(float(isPositive) / (len(test_predictions) + len(train_predictions)))
'''
log_scale = []
start = 1e-5
for i in range(10):
  log_scale.append(start)
  start *= 10

train_err = []
test_err = []
bestC = 0
bestGamma = 0
bestAccuracy = 0
for i in log_scale:
  test_arr = []
  train_arr = []
  for j in log_scale:
    classifier = SVC(C=j, gamma=i)
    classifier.fit(train_x, train_y)

    train_predictions = classifier.predict(train_x)
    test_predictions = classifier.predict(test_x)

    right_train = 0
    for k in range(len(train_predictions)):
      if train_predictions[k] == train_y[k]:
        right_train += 1
    train_arr.append(float(right_train) / len(train_predictions))

    right_test = 0
    for k in range(len(test_predictions)):
      if test_predictions[k] == test_y[k]:
        right_test += 1
    if bestAccuracy < float(right_test) / len(test_predictions):
      bestGamma = i
      bestC = j
      bestAccuracy = float(right_test) / len(test_predictions)
    test_arr.append(float(right_test) / len(test_predictions))
  train_err.append(train_arr)
  test_err.append(test_arr)
'''plt.plot(gammas, train_err)
plt.plot(gammas, test_err)'''
plt.imshow(test_err, cmap=plt.cm.Reds, interpolation='none', extent=[-5, 5, -5, 5])
plt.colorbar()
plt.ylabel('Gamma (log)')
plt.xlabel('C (log)')
plt.show()

print bestGamma
print bestC
