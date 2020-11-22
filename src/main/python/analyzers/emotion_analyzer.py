import pandas as pd
from nrclex import NRCLex


def __getEmotions(text):
    """
    Get emotion affect frequencies for the input text. The values returned are continuous numbers between 0 & 1.
    Values are returned for the following emotions: fear, anger, trust, surprise, sadness, disgust, joy, anticipation

    :param text: the input text
    :return: a dict with a continuous value between 0-1 for each emotion
    """
    textObject = NRCLex(text)
    emtionsDict = textObject.affect_frequencies
    if 'anticipation' not in emtionsDict:
        emtionsDict['anticipation'] = 0.0
    [emtionsDict.pop(key) for key in ['positive', 'negative', 'anticip']]
    return emtionsDict


def getEmotionAnalysis(dataframe):
    """
    Add emotion columns to dataframe

    :param dataframe: player dataframe with tweet column
    :return: A pandas dataframe with the emotion affects appended to the original dataframe
    """
    return dataframe.join(pd.DataFrame([__getEmotions(row.Tweet) for i, row in dataframe.iterrows()],
                                       index=[i for i, row in dataframe.iterrows()]))
