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

    # def getSentimentAnalysis(self, tweetsList: list.__class__, regression=True):
    def getSentimentAnalysis(self, regression='1'):
        # resultsDF = sa.getSentimentAnalysis(tweetsList)
        resultsDF = sa.getSentimentAnalysis(self.tweetsAndStatsDF.copy())
        # featureColumnIndexes = ['positive', 'neutral', 'ngeative']
        # Combine resultsDF with self.tweetsAndStats.copy()
        # if regression == '1':
        #     resultsDictOrDF = self.__performRegressionAnalysis(resultsDF, featureColumnIndexes)
        # elif regression == '2':
        #     resultsDictOrDF = self.__performMLPAnalysis(resultsDF, featureColumnIndexes)
        # else:
        #     resultsDictOrDF = self.__performRandomForestAnalysis(resultsDF, featureColumnIndexes)
        # return resultsDictOrDF

    def getEmotionAnalysis(self, regression='1'):
        resultsDF = ea.getEmotionAnalysis(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = ['fear', 'anger', 'trust', 'surprise', 'sadness', 'disgust', 'joy', 'anticipation']
        # Combine resultsDF with self.tweetsAndStats.copy()
        if regression == '1':
            resultsDictOrDF = self.__performRegressionAnalysis(resultsDF, featureColumnIndexes)
        elif regression == '2':
            resultsDictOrDF = self.__performMLPAnalysis(resultsDF, featureColumnIndexes)
        else:
            resultsDictOrDF = self.__performRandomForestAnalysis(resultsDF, featureColumnIndexes)
        return resultsDictOrDF

    def getEmbeddedAnalysis(self, regression='1'):
        resultsDF = emb.getSentenceEmbeddingAsDF(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = [col for col in resultsDF.columns if col.startswith('embedding')]
        # Combine resultsDF with self.tweetsAndStats.copy()
        if regression == '1':
            resultsDictOrDF = self.__performRegressionAnalysis(resultsDF, featureColumnIndexes)
        elif regression == '2':
            resultsDictOrDF = self.__performMLPAnalysis(resultsDF, featureColumnIndexes)
        else:
            resultsDictOrDF = self.__performRandomForestAnalysis(resultsDF, featureColumnIndexes)
        return resultsDictOrDF

    def getCombinationAnalysis(self, tweetsList: list.__class__, regression=True):
        sentDF = sa.getSentimentAnalysis(tweetsList)
        emotDF = ea.getEmotionAnalysis(self.tweetsAndStatsDF)
        # embedDF = ema.getEmbeddedAnalysis(self.tweetsAndStatsDF)
        # combine these three dfs with self.tweetsAndStats.copy()
        # if regression:
        #     resultsDictOrDF = __performRegressionAnalysis(combinedDF, featureColumnIndexes)
        # else:
        #     resultsDictOrDF = __performOtherAnalysis(combinedDF, featureColumnIndexes)
        # return resultsDictOrDF

    def __performRegressionAnalysis(self, dfWithFeatures, featureColumnIndexes):
        """
        Performs regression analysis after the initial analysis

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @return: A dataframe of measurements of how well regression worked for the given dataframe
        @rtype: dictionary
        """
        # Perform regression analysis
        X = dfWithFeatures[featureColumnIndexes]
        y = dfWithFeatures['PlusMinusPoints']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Generating models
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        prediction = lr.predict(X_test)
        resultsDictOrDF = pd.concat([y_test, pd.Series(prediction, index=y_test.index, name='y_test')], axis=1)
        resultsDictOrDF.columns = ['y_pred', 'y_test']
        return resultsDictOrDF

    def __performMLPAnalysis(self, dfWithFeatures, featureColumnIndexes):
        """
        Performs whatever other analysis after the initial analysis

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @return: A dataframe of measurements of how well the other model worked for the given dataframe
        @rtype: Dataframe
        """
        # Perform regression analysis
        X = dfWithFeatures[featureColumnIndexes]
        y = dfWithFeatures['PlusMinusPoints']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Generating models
        mlpc = MLPRegressor(hidden_layer_sizes=(100, 200, 100), activation='relu',
                            max_iter=10000, solver='adam', alpha=0.005, learning_rate_init=0.001,
                            shuffle=False)
        mlpc.fit(X_train, y_train)
        prediction = mlpc.predict(X_test)
        resultsDictOrDF = pd.concat([y_test, pd.Series(prediction, index=y_test.index, name='y_test')], axis=1)
        resultsDictOrDF.columns = ['y_pred', 'y_test']
        return resultsDictOrDF

    def __performRandomForestAnalysis(self, dfWithFeatures, featureColumnIndexes):
        """
        Performs whatever other analysis after the initial analysis

        @param dfWithFeatures: The data frame that will have the features from an analysis
        @param featureColumnIndexes: A list of the indexes that contain the feature columns
        @return: A dataframe of measurements of how well the other model worked for the given dataframe
        @rtype: Dataframe
        """
        # Perform regression analysis
        X = dfWithFeatures[featureColumnIndexes]
        y = dfWithFeatures['PlusMinusPoints']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        # Generating models
        randomForest = RandomForestRegressor(n_estimators=1000)
        randomForest.fit(X_train, y_train)
        prediction = randomForest.predict(X_test)
        resultsDictOrDF = pd.concat([y_test, pd.Series(prediction, index=y_test.index, name='y_test')], axis=1)
        resultsDictOrDF.columns = ['y_pred', 'y_test']
        return resultsDictOrDF
