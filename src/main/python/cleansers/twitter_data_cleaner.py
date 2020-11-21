from nltk import WordNetLemmatizer, pos_tag
from pandas import DataFrame
from nltk.corpus import stopwords
import numpy as np
import re
import nltk
# nltk.download('stopwords')  # Uncomment if needed
# nltk.download("punkt")  # Uncomment if needed

# import pandas as pd  # test only
# import loaders.twitter_data_loader as tdl  # for test code

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
    cleanDF = df.copy()
    # removes URLs, then mentions, then hashtags, then punctuation,
    # then newlines, then emojis, converts everything to lowercase,
    # removes stopping words, then removes excess spacing.
    # Lastly, empty tweets are removed. The order is important.
    cleanDF['Tweet'] = df['Tweet'].map(lambda tweet: re.sub(r'http\S+', '', tweet)) \
        .map(lambda tweet: re.sub(r'@[A-Za-z0-9_]+', '', tweet)) \
        .map(lambda tweet: re.sub(r'#[A-Za-z0-9_]+', '', tweet)) \
        .map(lambda tweet: re.sub(r'[^a-zA-z0-9\s]', '', tweet)) \
        .map(lambda tweet: re.sub(r'\n', '', tweet)) \
        .map(lambda tweet: emoji_regrex_pattern.sub(r'', tweet)) \
        .map(lambda tweet: tweet.lower()) \
        .map(lambda tweet: re.sub(stopwordsRegexPattern, '', tweet)) \
        .map(lambda tweet: __getLemmatizedTweet(tweet)) \
        .map(lambda tweet: __removeExcessiveSpace(tweet))
    cleanDF = cleanDF.replace(r'^\s*$', np.nan, regex=True)
    cleanDF = cleanDF.dropna(subset=['Tweet'])
    cleanDF['TweetDate'] = cleanDF['TweetDate'].map(lambda date: date.date())
    cleanDF = cleanDF.sort_values('TweetDate')
    return cleanDF


def __getLemmatizedTweet(tweet: str):
    tokenizedWordsInTweet = nltk.word_tokenize(tweet)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tweet = ""
    for word, tag in pos_tag(tokenizedWordsInTweet):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_tweet += " " + lemmatizer.lemmatize(word, pos)
    return lemmatized_tweet


def __removeExcessiveSpace(tweet: str):
    while "  " in tweet:
        tweet = tweet.replace("  ", " ")
        tweet.strip()
    return tweet


# pd.set_option('display.max_columns', None)
# tweetsDF = tdl.getPlayerTweetsAsDF('KingJames', '2018-10-12', '2019-04-10')
# print(tweetsDF['Tweet'])
# tweetsDF = cleanTweets(tweetsDF)
# print('\nCleaned Tweet\n', tweetsDF['Tweet'])
