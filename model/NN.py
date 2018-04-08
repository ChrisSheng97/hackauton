import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import csv
from sklearn import metrics
from sklearn.model_selection import KFold, StratifiedKFold

kf = KFold(n_splits=10)
# 90% CI, t distribution
Z = 1.833

# model
class NN():
    def __init__(self, X, Y, lr=0.000001):
        num_feature = len(X[0])
        output_num = len(Y[0])
        print(output_num)
        self.X = np.array(X)
        self.Y = np.array(Y)
        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(num_feature,), activation='relu'))
        self.model.add(Dense(output_num, activation='softmax'))
        self.model.compile(loss='binary_crossentropy', optimizer=Adam(lr = lr), metrics=['accuracy'])

        self.train_steps = 1000
        self.scores = []


    def train(self):
        for train_index, test_index in kf.split(self.X):
            # print(self.X, train_index)
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.Y[train_index], self.Y[test_index]

            # for t in range(self.train_steps):
            self.model.fit(X_train, y_train)
            score = self.model.evaluate(X_test, y_test)
            print(score)
            self.scores.append(score)


