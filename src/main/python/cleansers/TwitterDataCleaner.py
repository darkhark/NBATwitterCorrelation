from pandas import DataFrame
from nltk.corpus import stopwords
import numpy as np
import re
# import nltk
# nltk.download('stopwords')  # Uncomment if needed
import loaders.TwitterDataLoader as tdl

emoji_regrex_pattern = re.compile(pattern="["
                                          u"\U0001F600-\U0001F64F"  # emoticons
                                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                          "]+", flags=re.UNICODE)


def cleanTweets(df: DataFrame.__class__) -> DataFrame.__class__:
    """
    Removes punctuation, emojis, excessive spacing, and stopping words and converts the
    the data to lowercase.

    @param df: The Dataframe received from the TwitterDataLoader
    @type df: Pandas Dataframe.
    @return: A Dataframe with cleansed tweets.
    @rtype: PandasDataframe
    """
    stopWords = stopwords.words('english')
    stopwordsRegexPattern = r'\b(?:{})\b'.format('|'.join(stopWords))
    cleanDF = df
    # removes URLs, then mentions, then hashtags, then punctuation,
    # then emojis, converts everything to lowercase,
    # removes stopping words, then removes excess spacing.
    # Lastly, empty tweets are removed. The order is important.
    cleanDF['tweet'] = df['tweet'].map(lambda tweet: re.sub(r'http\S+', '', tweet)) \
        .map(lambda tweet: re.sub(r'@[A-Za-z0-9_]+', '', tweet)) \
        .map(lambda tweet: re.sub(r'#[A-Za-z0-9_]+', '', tweet)) \
        .map(lambda tweet: re.sub(r'[^a-zA-z0-9\s]', '', tweet)) \
        .map(lambda tweet: emoji_regrex_pattern.sub(r'', tweet)) \
        .map(lambda tweet: tweet.lower()) \
        .map(lambda tweet: re.sub(stopwordsRegexPattern, '', tweet)) \
        .map(lambda tweet: removeExcessiveSpace(tweet))
    cleanDF.apply(lambda x: np.nan if isinstance(x, str) and (x.isspace() or not x) else x)
    cleanDF.dropna(subset=['tweet'], inplace=True)
    return cleanDF


def removeExcessiveSpace(tweet):
    while "  " in tweet:
        tweet = tweet.replace("  ", " ")
    return tweet

# tweetsDF = tdl.getPlayerTweetsAsDF('KingJames', '2018-10-12', '2019-04-10')
# print(tweetsDF)
# tweetsDF = cleanTweets(tweetsDF)
# print(tweetsDF)
