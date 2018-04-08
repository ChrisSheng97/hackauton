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

# load dataset and split into train and test datasets
# use 10-fild cross validation to train 

X = []
Y = []
with open('synthetic_encoded.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        X.append(row[:-1])
        Y.append(row[-1])
        print(row)

X = np.array(X)
Y = np.array(Y)

# model
class NN():
    def __init__(self, num_feature, lr=0.000001):
        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(num_feature,), activation='relu'))
        self.model.add(Dense(1, activation='softmax'))
        self.model.compile(loss='binary_crossentropy', optimizer=Adam(lr = lr), metrics=['accuracy'])

        self.train_steps = 1000
        self.scores = []

    def train(self):
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = Y[train_index], Y[test_index]

            # for t in range(self.train_steps):
            self.model.fit(X_train, y_train)
            score = self.model.evaluate(X_test, y_test)
            print(score)
            self.scores.append(score)

    # def predict(self):
    #     predictions = self.model.predict(X)
    #     print(predictions)

def main(args): 
    model = NN(30)
    model.train()
    # model.predict()

if __name__ == '__main__':
    main(sys.argv)

