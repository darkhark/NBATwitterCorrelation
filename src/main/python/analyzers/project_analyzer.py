import pandas as pd
import analyzers.sentiment_analyzer as sa
import analyzers.embedded_analyzer as emb
import analyzers.emotion_analyzer as ea
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor


class TweetsAnalyzer:
    def __init__(self, tweetsAndStatsDF):
        self.tweetsAndStatsDF = tweetsAndStatsDF

    def getSentimentAnalysis(self, points, regressionMethod='1'):
        resultsDF = sa.getSentimentAnalysis(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = ['neutral', 'negative', 'positive']
        # Combine resultsDF with self.tweetsAndStats.copy()
        if regressionMethod == '1':
            resultsDF = self.__performRegressionAnalysis(resultsDF, featureColumnIndexes, points)
        elif regressionMethod == '2':
            resultsDF = self.__performMLPAnalysis(resultsDF, featureColumnIndexes, points)
        else:
            resultsDF = self.__performRandomForestAnalysis(resultsDF, featureColumnIndexes, points)
        return resultsDF

    def getEmotionAnalysis(self, points, regressionMethod='1'):
        resultsDF = ea.getEmotionAnalysis(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = ['fear', 'anger', 'trust', 'surprise', 'sadness', 'disgust', 'joy', 'anticipation']
        # Combine resultsDF with self.tweetsAndStats.copy()
        if regressionMethod == '1':
            resultsDF = self.__performRegressionAnalysis(resultsDF, featureColumnIndexes, points)
        elif regressionMethod == '2':
            resultsDF = self.__performMLPAnalysis(resultsDF, featureColumnIndexes, points)
        else:
            resultsDF = self.__performRandomForestAnalysis(resultsDF, featureColumnIndexes, points)
        return resultsDF

    def getEmbeddedAnalysis(self, points, regressionMethod='1'):
        resultsDF = emb.getSentenceEmbeddingAsDF(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = [col for col in resultsDF.columns if col.startswith('embedding')]
        # Combine resultsDF with self.tweetsAndStats.copy()
        if regressionMethod == '1':
            resultsDF = self.__performRegressionAnalysis(resultsDF, featureColumnIndexes, points)
        elif regressionMethod == '2':
            resultsDF = self.__performMLPAnalysis(resultsDF, featureColumnIndexes, points)
        else:
            resultsDF = self.__performRandomForestAnalysis(resultsDF, featureColumnIndexes, points)
        return resultsDF

    def getCombinationAnalysis(self, points, regressionMethod='1'):
        # get sentiment features
        resultsDF = sa.getSentimentAnalysis(self.tweetsAndStatsDF.copy())
        # get emotion features
        resultsDF = ea.getEmotionAnalysis(resultsDF)
        # get embedding features
        resultsDF = emb.getSentenceEmbeddingAsDF(resultsDF)
        # define feature columns
        sentColumnIndexes = ['neutral', 'negative', 'positive']
        emotColumnIndexes = ['fear', 'anger', 'trust', 'surprise', 'sadness', 'disgust', 'joy', 'anticipation']
        embdColumnIndexes = [col for col in resultsDF.columns if col.startswith('embedding')]
        featureColumnIndexes = sentColumnIndexes + emotColumnIndexes + embdColumnIndexes
        # combine these three dfs with self.tweetsAndStats.copy()
        if regressionMethod == '1':
            resultsDF = self.__performRegressionAnalysis(resultsDF, featureColumnIndexes, points)
        elif regressionMethod == '2':
            resultsDF = self.__performMLPAnalysis(resultsDF, featureColumnIndexes, points)
        else:
            resultsDF = self.__performRandomForestAnalysis(resultsDF, featureColumnIndexes, points)
        return resultsDF

    def __performRegressionAnalysis(self, dfWithFeatures, featureColumnIndexes, points: bool):
        """
        Performs regression analysis using linear regression

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @param points: True if points should be predicted, false if accuracy should be predicted.
        @return: A dataframe of measurements of how well linear regression worked for the given dataframe
        @rtype: dictionary
        """
        X = dfWithFeatures[featureColumnIndexes]
        if points:
            y = dfWithFeatures['PlusMinusPoints']
        else:
            y = dfWithFeatures['PlusMinusAcc']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Generating models
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        prediction = lr.predict(X_test)
        resultsDF = pd.DataFrame(y_test.rename('y_test')).join(
            pd.DataFrame(pd.Series(prediction, index=y_test.index, name='y_pred')))
        return resultsDF

    def __performMLPAnalysis(self, dfWithFeatures, featureColumnIndexes, points):
        """
        Performs a regression analysis using an MLP NN

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @param points: True if points should be predicted, false if accuracy should be predicted.
        @return: A dataframe of measurements of how well the MLP model worked for the given dataframe
        @rtype: Dataframe
        """
        X = dfWithFeatures[featureColumnIndexes]
        if points:
            y = dfWithFeatures['PlusMinusPoints']
        else:
            y = dfWithFeatures['PlusMinusAcc']
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

    def __performRandomForestAnalysis(self, dfWithFeatures, featureColumnIndexes, points):
        """
        Performs a regression analysis using an a random forest

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @param points: True if points should be predicted, false if accuracy should be predicted.
        @return: A dataframe of measurements of how well the random forest model worked for the given dataframe
        @rtype: Dataframe
        """
        X = dfWithFeatures[featureColumnIndexes]
        if points:
            y = dfWithFeatures['PlusMinusPoints']
        else:
            y = dfWithFeatures['PlusMinusAcc']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Generating models
        randomForest = RandomForestRegressor(n_estimators=1000)
        randomForest.fit(X_train, y_train)
        prediction = randomForest.predict(X_test)
        resultsDF = pd.DataFrame(y_test.rename('y_test')).join(
            pd.DataFrame(pd.Series(prediction, index=y_test.index, name='y_pred')))
        return resultsDF
