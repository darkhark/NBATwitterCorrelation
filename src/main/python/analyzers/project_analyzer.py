import analyzers.sentiment_analyzer as sa
import analyzers.embedded_analyzer as emb
import analyzers.emotion_analyzer as ea
from modelers.regression_models import *


class TweetsAnalyzer:
    def __init__(self, tweetsAndStatsDF):
        self.tweetsAndStatsDF = tweetsAndStatsDF

    def getSentimentAnalysis(self, points, regressionMethod='1'):
        resultsDF = sa.getSentimentAnalysis(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = ['neutral', 'negative', 'positive']
        regressionModel = TweetsModeler.getModelResutls(resultsDF, featureColumnIndexes, points, regressionMethod)
        return regressionModel

    def getEmotionAnalysis(self, points, regressionMethod='1'):
        resultsDF = ea.getEmotionAnalysis(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = ['fear', 'anger', 'trust', 'surprise', 'sadness', 'disgust', 'joy', 'anticipation']
        regressionModel = TweetsModeler.getModelResutls(resultsDF, featureColumnIndexes, points, regressionMethod)
        return regressionModel

    def getEmbeddedAnalysis(self, points, regressionMethod='1'):
        resultsDF = emb.getSentenceEmbeddingAsDF(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = [col for col in resultsDF.columns if col.startswith('embedding')]
        regressionModel = TweetsModeler.getModelResutls(resultsDF, featureColumnIndexes, points, regressionMethod)
        return regressionModel

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
        regressionModel = TweetsModeler.getModelResutls(resultsDF, featureColumnIndexes, points, regressionMethod)
        return regressionModel
