import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import csv
from sklearn import metrics
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import mean_squared_error
import copy

kf = KFold(n_splits=10)
# 90% CI, t distribution
Z = 1.833

# model
class NN():
    def __init__(self, X, Y, lr=0.0001):
        num_feature = len(X[0])
        output_num = len(Y[0])
        print(output_num)
        self.X = np.array(X)
        self.Y = np.array(Y)
        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(num_feature,), activation='relu'))
        self.model.add(Dense(output_num, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer=Adam(lr = lr), metrics=['accuracy'])

        self.train_steps = 1000
        self.scores = []


    def train(self):
        for train_index, test_index in kf.split(self.X):
            # print(self.X, train_index)
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.Y[train_index], self.Y[test_index]
            self.X_test = X_test
            self.y_test = y_test

            # for t in range(self.train_steps):
            self.model.fit(X_train, y_train)
            self.predict(X_test, y_test)
    
    def predict(self, X_test, y_test):
        prediction = self.model.predict(X_test)
        bin_prediction = []
        for pred in prediction:
            if pred[-1] > 0.5: # yes, OD
                bin_prediction.append(1)
            else:
                bin_prediction.append(0)
        test_pred = []
        for y_t in y_test:
            if y_t[-1] == 0: # yes, OD
                test_pred.append(1)
            else:
                test_pred.append(0)
        accur = []
        for i in range(len(bin_prediction)):
            if bin_prediction[i] == test_pred[i]:
                accur.append(1)
            else:
                accur.append(0)
        acc = float(np.sum(np.array(accur))) / float(len(accur))

class Bin_NN():
    def __init__(self, X, Y, lr=0.0001):
        num_feature = len(X[0])
        output_num = len(Y[0])
        self.X = np.array(X)
        self.Y = np.array(Y)
        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(num_feature,), activation='relu'))
        self.model.add(Dense(1, activation='softmax'))
        self.model.compile(loss='mse', optimizer=Adam(lr = lr), metrics=['accuracy'])

        self.train_steps = 1000
        self.scores = []

    def train(self):
        for train_index, test_index in kf.split(self.X):
            # print(self.X, train_index)
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.Y[train_index], self.Y[test_index]
            self.X_test = X_test
            self.y_test = y_test

            # for t in range(self.train_steps):
            self.model.fit(X_train, y_train)
            score = self.model.evaluate(X_test, y_test)
            self.scores.append(score)

    def gen_rand_test_data(self, num_test):
        X_ = copy.deepcopy(self.X)
        Y_ = copy.deepcopy(self.Y)
        X_test = np.random.choice(X_.flatten(), num_test)
        y_test = np.random.choice(Y_.flatten(), num_test)
        self.predict(X_test, y_test)

    def predict(self, X_test, y_test):
        prediction = self.model.predict(X_test)
        bin_prediction = []
        for pred in prediction:
            if pred[-1] > 0.5: # yes, OD
                bin_prediction.append(1)
            else:
                bin_prediction.append(0)
        test_pred = []
        for y_t in y_test:
            if y_t[-1] == 0: # yes, OD
                test_pred.append(1)
            else:
                test_pred.append(0)
        accur = []
        for i in range(len(bin_prediction)):
            if bin_prediction[i] == test_pred[i]:
                accur.append(1)
            else:
                accur.append(0)
        acc = float(np.sum(np.array(accur))) / float(len(accur))
        print('accuracy: {}'.format(acc))

