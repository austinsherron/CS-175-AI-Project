import svm

X = [[1, 3], [2, 4], [1, 4], [2, 3], [3, 1], [4, 1], [4, 2], [3, 2]]
Y = [1, 1, 1, 1, -1, -1, -1, -1]

W, bias = svm.train_svm_parameters(X, Y)

print W
print bias
