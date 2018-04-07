import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy

# load dataset and split into train and test datasets
# use 10-fild cross validation to train 

# model
class NN():
    def __init__(self, num_feature, lr=0.0001):
        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(num_feature,), activation='relu'))
        self.model.add(Dense(32, activation='softmax'))
        self.model.compile(loss='binary_crossentropy', optimizer=Adam(lr = lr), metrics=['accuracy'])

        self.train_steps = 1000
        self.scores = []

    def train(self):
        # for i in range(self.train_steps):
        #     model.fit(X, Y, epochs=1, batch_size=32)
        #     score = model.evaluate(X, Y)
        #     print(score)
        #     self.scores.append(score)
        pass

    def predict(self):
        # predictions = model.predict(X)
        # print(predictions)
        pass


def main(args): 
    model = NN(10)
    model.train()
    model.predict()

if __name__ == '__main__':
    main(sys.argv)

