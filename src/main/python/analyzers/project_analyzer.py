import analyzers.sentiment_analyzer as sa
import analyzers.emotion_analyzer as ea
import pandas as pd


class TweetsAnalyzer:
    def __init__(self, tweetsAndStatsDF):
        self.tweetsAndStatsDF = tweetsAndStatsDF

    def getSentimentAnalysis(self, tweetsList: list.__class__, regression=True):
        resultsDF = sa.getSentimentAnalysis(tweetsList)
        print("Results\n", resultsDF.index)
        mergedDF = pd.merge(
            left=self.tweetsAndStatsDF.copy(),
            right=resultsDF,
            left_index=True,
            right_index=True
        )
        print("Merged\n", mergedDF)
        # if regression:
        #     resultsDictOrDF = __performRegressionAnalysis(resultsDF, featureColumnIndexes))
        # else:
        #     resultsDictOrDF = __performOtherAnalysis(resultsDF, featureColumnIndexes)
        # return resultsDictOrDF

    def getEmotionAnalysis(self, regression=True):
        resultsDF = ea.getEmotionAnalysis(self.tweetsAndStatsDF.copy())
        # Combine resultsDF with self.tweetsAndStats.copy()
        # if regression:
        #     resultsDictOrDF = __performRegressionAnalysis(resultsDF, featureColumnIndexes))
        # else:
        #     resultsDictOrDF = __performOtherAnalysis(resultsDF, featureColumnIndexes)
        # return resultsDictOrDF

    # def getEmbeddedAnalysis(self, regression=True):
        # resultsDF = the embedded method for getting the dataframe
        # Combine resultsDF with self.tweetsAndStats.copy()
        # if regression:
        #     resultsDictOrDF = __performRegressionAnalysis(resultsDF, featureColumnIndexes))
        # else:
        #     resultsDictOrDF = __performOtherAnalysis(resultsDF, featureColumnIndexes)
        # return resultsDictOrDF

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
        # return resultsDictOrDF

    # def __performOtherAnalysis(self, dfWithFeatures, featureColumnIndexes):
    #     """
    #     Performs whatever other analysis after the initial analysis
    #
    #     @param dfWithFeatures: The data frame that will have the features from an analysis
    #     @param featureColumnIndexes: A list of the indexes that contain the feature columns
    #     @return: A dataframe of measurements of how well the other model worked for the given dataframe
    #     @rtype: Dataframe
    #     """
    #     Perform one other type of analysis
    #     return resultsDictOrDF
