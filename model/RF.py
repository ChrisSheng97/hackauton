import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.tree import export_graphviz
import csv
import numpy as np

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

class RF():
    def __init__(self, max_depth):
        self.clf = RandomForestClassifier(max_depth=max_depth, random_state=0)
        self.train_steps = 100
        self.scores = []

    def train(self):
        for i in range(self.train_steps):
            self.clf.fit(X, Y)
            # clf = self.clf.fit(X, Y)
            # for tree in clf.estimators_:
            #     export_graphviz(tree, out_file='tree.dot')

            score = self.clf.score(X, Y)
            print(score)
            self.scores.append(score)
            


def main(args): 
    model = RF(100)
    model.train()


if __name__ == '__main__':
    main(sys.argv)