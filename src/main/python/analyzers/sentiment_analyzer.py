import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

def __getSentiment(tweet):
    """
    Get sentiment for the input text. The values returned are continuous numbers between 0 & 1.
    Values are returned for the following sentiments: neutral, negative, positive

    :param text: the input text
    :return: a dict with a continuous value between 0-1 for each emotion
    """
    sentiment = sid.polarity_scores(tweet)
    sentimentDict = {'neutral': sentiment['neu'], 'negative': sentiment['neg'], 'positive': sentiment['pos']}
    return sentimentDict


def getSentimentAnalysis(dataframe):
    """
    Add sentiments columns to dataframe

    :param dataframe: player dataframe with tweet column
    :return: A pandas dataframe with the sentiments appended to the original dataframe
    """
    return dataframe.join(pd.DataFrame([__getSentiment(row.Tweet) for i, row in dataframe.iterrows()],
                                       index=[i for i, row in dataframe.iterrows()]))