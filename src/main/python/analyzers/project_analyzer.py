import analyzers.sentiment_analyzer as sa
import analyzers.embedded_analyzer as emb
import analyzers.emotion_analyzer as ea
from modelers.regression_models import *
import plotly.express as px


class TweetsAnalyzer:
    def __init__(self, tweetsAndStatsDF):
        self.tweetsAndStatsDF = tweetsAndStatsDF
        self.sentimentPlot = None
        self.emotionPlot = None
        self.embeddingPlot = None

    def getSentimentAnalysis(self, points, regressionMethod='1'):
        resultsDF = sa.getSentimentAnalysis(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = ['neutral', 'negative', 'positive']
        regressionModel = TweetsModeler.getModelResutls(resultsDF, featureColumnIndexes, points, regressionMethod)
        df = pd.DataFrame(resultsDF[featureColumnIndexes].idxmax(axis=1).value_counts(), columns=['values'])
        self.sentimentPlot = px.pie(df, values='values', names=df.index, title='Postive/Negative/Neutral Proportion')
        return regressionModel

    def getEmotionAnalysis(self, points, regressionMethod='1'):
        resultsDF = ea.getEmotionAnalysis(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = ['fear', 'anger', 'trust', 'surprise', 'sadness', 'disgust', 'joy', 'anticipation']
        regressionModel = TweetsModeler.getModelResutls(resultsDF, featureColumnIndexes, points, regressionMethod)
        df = resultsDF[['TweetDate'] + featureColumnIndexes].melt(id_vars='TweetDate')
        df['TweetDate'] = df['TweetDate'].apply(str)
        self.emotionPlot = px.line(df, x="TweetDate", y="value", color="variable", title='Emotions Through Time')
        self.emotionPlot.layout.xaxis.type = 'category'
        return regressionModel

    def getEmbeddedAnalysis(self, points, regressionMethod='1'):
        resultsDF = emb.getSentenceEmbeddingAsDF(self.tweetsAndStatsDF.copy())
        featureColumnIndexes = [col for col in resultsDF.columns if col.startswith('embedding')]
        regressionModel = TweetsModeler.getModelResutls(resultsDF, featureColumnIndexes, points, regressionMethod)
        average_length = np.mean(resultsDF.Tweet.apply(str.split).apply(len))
        num_features = resultsDF[featureColumnIndexes].shape[1]
        df = pd.DataFrame([average_length, num_features], index=['average_length', 'num_features'], columns=['values'])
        self.embeddingPlot = px.bar(df, x=df.index, y='values', color=df.index, title='Average Tweet Length vs. Number of Features')
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
