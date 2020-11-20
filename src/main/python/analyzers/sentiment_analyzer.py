import pandas as pd
# pip install --upgrade azure-ai-textanalytics
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextDocumentInput

_key = "adc96f39ac2a4918a1f462b5bf8674b8"
_endpoint = "https://nbatwittersentiment.cognitiveservices.azure.com/"


def __authenticate(key:str, endpoint:str):
    # Authentication
    ta_credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential,
        api_version='TextAnalyticsApiVersion.V3_0')
    return client


def __formatresponse(responseList) -> pd.DataFrame:
    """
    The return value for a single document can be a result or error object.
    A heterogeneous list containing a collection of result and error objects is returned
    from each operation. These results/errors are index-matched with the order of the provided documents
    """
    cleanresponse = {'tweetID': responseList.id,
                     'positive': responseList.confidence_scores.positive,
                     'neutral': responseList.confidence_scores.neutral,
                     'negative': responseList.confidence_scores.negative
                     }
    for idx, sentence in enumerate(responseList.sentences):
        cleanresponse['tweet'] = sentence.text
    sentiment_df = pd.DataFrame.from_records(cleanresponse, index=[0])
    return sentiment_df

'''
def getSentimentAnalysis(tweet: list.__class__) -> pd.DataFrame:
    """
    Uses Microsoft Cognitive Service Text Analytics 3.0 to analyze text

    @param tweet: A list of TextDocumentInput where the id is the tweetID and text is the tweet. English is the default
    language.
    @return: A dataframe containing columns negative, neutral, positive,tweet,tweetID with a made up index
    @rtype: Dataframe
    """
    tweets = tweet
    client = __authenticate(_key, _endpoint)
    response = client.analyze_sentiment(documents=tweets)[0]
    tweetdf = __formatresponse(response)
    return tweetdf
'''

def getSentimentAnalysis(dataframe):
    """
    Uses Microsoft Cognitive Service Text Analytics 3.0 to analyze text

    @param tweet: A list of TextDocumentInput where the id is the tweetID and text is the tweet. English is the default
    language.
    @return: A dataframe containing columns negative, neutral, positive,tweet,tweetID with a made up index
    @rtype: Dataframe
    """
    documents = []
    for i, row in dataframe.iterrows():
        documents.append({"id": i, "language": "en", "text": row.Tweet})
    client = __authenticate(_key, _endpoint)
    response = client.analyze_sentiment(documents=documents)[0]
    tweetdf = __formatresponse(response)
    return tweetdf


# Test code
# textDocument = TextDocumentInput(id="746573683658463839", text="I am scoring some points in tonight's game")
# tweetAnalyzer = sentiment_analysis(textDocument)
# print(tweetAnalyzer)

# Possible solution
# documents = []
# for i, row in allTweetsAndStatsDF.iterrows():
#     documents.append({"id": i, "language": "en", "text": row.Tweet})
#
# response = client.analyze_sentiment(documents=documents)[0]
