import numpy as np
import pandas as pd
from argparse import Namespace
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error


class TweetsModeler:
    def __init__(self, args):
        self.dfWithFeatures = args.dfWithFeatures
        self.featureColumnIndexes = args.featureColumnIndexes
        self.points = args.points
        self.regressionMethod = args.regressionMethod
        self.regResultsDF = pd.DataFrame()
        self.resultsDict = dict()

    @classmethod
    def getModelResutls(cls, dfWithFeatures, featureColumnIndexes, points, regressionMethod):
        """
        Returns an object with attr

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @param points: True if points should be predicted, false if accuracy should be predicted.
        @param regressionMethod: An integer value signalling which regression method to be used
        @return: An object with attributes for results dataframe and regression results
        @rtype: object
        """
        args = Namespace(
            dfWithFeatures=dfWithFeatures,
            featureColumnIndexes=featureColumnIndexes,
            points=points,
            regressionMethod=regressionMethod,
        )
        tweetsModeler = cls(args)
        if tweetsModeler.regressionMethod == '1':
            tweetsModeler.regResultsDF = tweetsModeler.performRegressionAnalysis()
        elif args.regressionMethod == '2':
            tweetsModeler.regResultsDF = tweetsModeler.performMLPAnalysis()
        else:
            tweetsModeler.regResultsDF = tweetsModeler.performRandomForestAnalysis()

        tweetsModeler.resultsDict = {
            'r2': r2_score(tweetsModeler.regResultsDF['y_test'], tweetsModeler.regResultsDF['y_pred']),
            'mse': mean_squared_error(tweetsModeler.regResultsDF['y_test'], tweetsModeler.regResultsDF['y_pred'])
        }
        return tweetsModeler

    def performRegressionAnalysis(self):
        """
        Performs regression analysis using linear regression

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @param points: True if points should be predicted, false if accuracy should be predicted.
        @return: A dataframe of measurements of how well linear regression worked for the given dataframe
        @rtype: dictionary
        """
        np.random.seed(0)
        X = self.dfWithFeatures[self.featureColumnIndexes]
        if self.points:
            y = self.dfWithFeatures['PlusMinusPoints']
        else:
            y = self.dfWithFeatures['PlusMinusAcc']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Generating models
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        prediction = lr.predict(X_test)
        resultsDF = pd.DataFrame(y_test.rename('y_test')).join(
            pd.DataFrame(pd.Series(prediction, index=y_test.index, name='y_pred')))
        return resultsDF

    def performMLPAnalysis(self):
        """
        Performs a regression analysis using an MLP NN

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @param points: True if points should be predicted, false if accuracy should be predicted.
        @return: A dataframe of measurements of how well the MLP model worked for the given dataframe
        @rtype: Dataframe
        """
        np.random.seed(0)
        X = self.dfWithFeatures[self.featureColumnIndexes]
        if self.points:
            y = self.dfWithFeatures['PlusMinusPoints']
        else:
            y = self.dfWithFeatures['PlusMinusAcc']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Generating models
        mlpc = MLPRegressor(hidden_layer_sizes=(100, 200, 100), activation='relu',
                            max_iter=10000, solver='adam', alpha=0.005, learning_rate_init=0.001,
                            shuffle=False)
        mlpc.fit(X_train, y_train)
        prediction = mlpc.predict(X_test)
        resultsDF = pd.DataFrame(y_test.rename('y_test')).join(
            pd.DataFrame(pd.Series(prediction, index=y_test.index, name='y_pred')))
        return resultsDF

    def performRandomForestAnalysis(self):
        """
        Performs a regression analysis using an a random forest

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @param points: True if points should be predicted, false if accuracy should be predicted.
        @return: A dataframe of measurements of how well the random forest model worked for the given dataframe
        @rtype: Dataframe
        """
        np.random.seed(0)
        X = self.dfWithFeatures[self.featureColumnIndexes]
        if self.points:
            y = self.dfWithFeatures['PlusMinusPoints']
        else:
            y = self.dfWithFeatures['PlusMinusAcc']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Generating models
        randomForest = RandomForestRegressor(n_estimators=1000)
        randomForest.fit(X_train, y_train)
        prediction = randomForest.predict(X_test)
        resultsDF = pd.DataFrame(y_test.rename('y_test')).join(
            pd.DataFrame(pd.Series(prediction, index=y_test.index, name='y_pred')))
        return resultsDF
