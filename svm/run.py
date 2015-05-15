from classifier import Classifier
import kernel
import numpy as np

X = [
  np.array([1, 1]),
  np.array([1, 2]),
  np.array([2, 1]),
  np.array([2, 2]),
  np.array([3, 3]),
  np.array([3, 4]),
  np.array([4, 3]),
  np.array([4, 4])
]

Y = np.array([
    'bottom', 'bottom', 'bottom', 'bottom',
    'top', 'top', 'top', 'top'
])

svm_classifier = Classifier(X, Y)

print svm_classifier.w
print svm_classifier.bias
for x in X:
  print svm_classifier.predict(x)
