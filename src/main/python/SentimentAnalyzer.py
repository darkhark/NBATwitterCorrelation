import pandas as pd
# pip install --upgrade azure-ai-textanalytics
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

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
    col_list = responseList.keys()
    cleanresponse = {'tweetID':responseList.id,
                    'positive':responseList.confidence_scores.positive,
                    'neutral':responseList.confidence_scores.neutral,
                    'negative':responseList.confidence_scores.negative
                    }
    for idx, sentence in enumerate(responseList.sentences):
        cleanresponse ['tweet']= sentence.text
    sentiment_df = pd.DataFrame.from_records(cleanresponse,index=[0])
    return sentiment_df

def sentiment_analysis(tweet) -> pd.DataFrame:
    """Uses Microsoft Cognitive Service Text Analytics 3.0 to analyze text
    @param tweet[] list:
    @return: A dataframe containing columns negative, neutral, positive,tweet,tweetID
    @rtype: Dataframe
    """
    if 'tweetID' in tweet.keys():
        tweets = [tweet]
        client = __authenticate(_key, _endpoint)
        response = client.analyze_sentiment(documents=tweets)[0]
        tweetdf = __formatresponse(response)
    else:
        print('tweetID is not present')
        tweetdf = pd.DataFrame()
    return tweetdf

# Test code
tweet = {
    "tweetID": "1",
    "text": "I am scoring some points in tonight's game"}
tweetAnalyzer = sentiment_analysis(tweet)
print(tweetAnalyzer)