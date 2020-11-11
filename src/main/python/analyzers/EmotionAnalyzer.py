import pandas as pd
from nrclex import NRCLex


def getEmotions(text):
    """
    Get emotion affect frequencies for the input text

    :param text: the input text
    :return: a dict with the following emtoins: fear, anger, trust, surprise, sadness, disgust, joy, anticipation
    """
    textObject = NRCLex(text)
    emtionsDict = textObject.affect_frequencies
    if 'anticipation' not in emtionsDict:
        emtionsDict['anticipation'] = 0.0
    [emtionsDict.pop(key) for key in ['positive', 'negative', 'anticip']]
    return emtionsDict


def addEmotions(dataframe):
    """
    Add emotion columns to dataframe

    :param dataframe: player dataframe with tweet column
    :return: A pandas dataframe with the emotion affects appended to the original dataframe
    """
    return pd.concat([dataframe, pd.DataFrame([getEmotions(row.tweet) for i, row in dataframe.iterrows()])], axis=1)
