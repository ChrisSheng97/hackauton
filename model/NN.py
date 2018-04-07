import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import csv

# load dataset and split into train and test datasets
# use 10-fild cross validation to train 

X = []
Y = []
with open('synthetic.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        
        row[0] = row[0].split(' ')
        for i in range(len(row[0])):
            row[0][i] = float(row[0][i])
        row = row[0]
        X.append(row[:-7])
        Y.append(row[-7:])
        print(row)

X = np.array(X)
Y = np.array(Y)

# model
class NN():
    def __init__(self, num_feature, lr=0.0001):
        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(num_feature,), activation='relu'))
        self.model.add(Dense(7, activation='softmax'))
        self.model.compile(loss='binary_crossentropy', optimizer=Adam(lr = lr), metrics=['accuracy'])

        self.train_steps = 1000
        self.scores = []

    def train(self):
        for i in range(self.train_steps):
            self.model.fit(X, Y, epochs=1, batch_size=32)
            score = self.model.evaluate(X, Y)
            print(score)
            self.scores.append(score)

    def predict(self):
        predictions = self.model.predict(X)
        print(predictions)

def main(args): 
    model = NN(21)
    model.train()
    model.predict()

if __name__ == '__main__':
    main(sys.argv)

