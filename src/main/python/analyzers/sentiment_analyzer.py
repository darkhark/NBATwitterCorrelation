import pandas as pd
# pip install --upgrade azure-ai-textanalytics
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

_key = "adc96f39ac2a4918a1f462b5bf8674b8"
_endpoint = "https://nbatwittersentiment.cognitiveservices.azure.com/"


def getSentimentAnalysis(tweets: list.__class__) -> pd.DataFrame:
    """
    Uses Microsoft Cognitive Service Text Analytics 3.0 to analyze text

    @param tweets: A list of TextDocumentInput where the id is the tweetID and text is the tweet. English is the default
    language.
    @return: A dataframe containing columns negative, neutral, positive with an index of tweetID
    @rtype: Dataframe
    """
    responseDF = pd.DataFrame()
    client = __authenticate(_key, _endpoint)
    for group in __chunker(tweets, 10):
        print("Group\n", group)
        response = client.analyze_sentiment(documents=group)
        if responseDF.empty:
            responseDF = __formatResponse(response)
        else:
            responseDF.append(__formatResponse(response))
    return responseDF


def __chunker(seq, size):
    # https://stackoverflow.com/a/434328/7658632
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def __authenticate(key:str, endpoint:str):
    # Authentication
    ta_credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential,
        api_version='TextAnalyticsApiVersion.V3_0')
    return client


def __formatResponse(responseList) -> pd.DataFrame:
    """
    Using the data retrieved from the Sentiment Analyzer, a formatted dataframe is returned containing the results
    and the original data. The results are appended to the end.
    @param responseList:
    @return:
    @rtype:
    """
    columns = ['positive', 'neutral', 'negative']
    cleanResponse = {}
    for response in responseList:
        cleanResponse[response.id] = [response.confidence_scores.positive,
                                      response.confidence_scores.neutral,
                                      response.confidence_scores.negative]
    sentiment_df = pd.DataFrame.from_dict(cleanResponse, orient='index', columns=columns)
    return sentiment_df


# Test code
# pd.set_option('display.max_columns', None)
# lebron = NBAPlayer('LeBron James')
# tweetAnalyzer = getSentimentAnalysis(lebron.getAllTweetsAsTextDocumentInputs())
# print(tweetAnalyzer)
