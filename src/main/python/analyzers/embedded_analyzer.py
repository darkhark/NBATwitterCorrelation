from pathlib import Path
import tensorflow_hub as hub
import pandas as pd


print('Loading global sentence embedder...')
# if you will be using the online version of the universal sentence encoder model, please note that it can take some time to download
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"

# if you will be using a local copy of the universal sentence encoder model, make sure a copy resides in the same directory hosting the NBATwitterCorrelation
# module_url = str(Path(__file__).parent.parent.parent.parent.parent.parent) + '/universal-sentence-encoder_4'

model = hub.load(module_url)
print("module %s loaded" % module_url)


def __getSentenceEmbedding(input):
    """
    Returns a sentence embedding 512-dimensional vector

    :param input: tweet text
    :return: a 512-dimensional tensor vector
    """
    return model([input])


def getSentenceEmbeddingAsDF(dataframe):
    """
    Add embedding columns to dataframe

    :param dataframe: player dataframe with tweet column
    :return: A pandas dataframe with the embeddings appended to the original dataframe
    """
    embeddingDf = pd.DataFrame()
    for i, row in dataframe.iterrows():
        embeddingDf = embeddingDf.append([pd.DataFrame(__getSentenceEmbedding(row.Tweet).numpy())], ignore_index=True)
    embeddingDf.index = dataframe.index
    columns = ['embedding_' + str(i) for i in range(512)]
    embeddingDf.columns = columns
    return dataframe.join(embeddingDf)
