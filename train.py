import argparse
import pathlib
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


parser = argparse.ArgumentParser(description="Optional classifier training")
parser.add_argument("--webclients", required=True, type=pathlib.Path)
parser.add_argument("--bots", required=True, type=pathlib.Path)
parser.add_argument("--output", required=True, type=pathlib.Path)

if __name__ == "__main__":

    args = parser.parse_args()
    print(args.bots)
    #raise NotImplementedError

    #declaring variables
    X_train = [[1]]
    Y_train = [1]

    #create/fill the training set
    #TODO

    #create and train/fit the classifier
    classifier = RandomForestClassifier()
    classifier.fit(X_train, Y_train)

    #save the trained classifier
    joblib.dump(classifier, args.output)


    #to load the classifier 
    #loaded_rf = joblib.load("path")