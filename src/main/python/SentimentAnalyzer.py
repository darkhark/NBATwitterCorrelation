import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

_key = "adc96f39ac2a4918a1f462b5bf8674b8"
_endpoint = "https://nbatwittersentiment.cognitiveservices.azure.com/"

def _authenticate(key:str,endpoint:str):
    # Authentication
    ta_credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential,
        api_version='TextAnalyticsApiVersion.V3_0')
    return client

def _formatresponse(responseDict) -> pd.DataFrame :
    col_list = responseDict.keys()
    cleanresponse = {'tweetID':responseDict.id,
                    'positive':responseDict.confidence_scores.positive,
                    'neutral':responseDict.confidence_scores.neutral,
                    'negative':responseDict.confidence_scores.negative
                    }
    for idx, sentence in enumerate(responseDict.sentences):
        cleanresponse ['tweet']= sentence.text
    # sentiment_df = pd.DataFrame.from_dict(cleanresponse,orient='index')
    sentiment_df = pd.DataFrame.from_records(cleanresponse,index=[0])
    return sentiment_df

def sentiment_analysis(tweet) -> pd.DataFrame:
    """Uses Microsoft Cognitive Service Text Analytics 3.0 to analyze text
    @param tweet[] list: a list of dictionary tweet objects
    @return: A dataframe containing columns negative, neutral, positive,tweet,tweetID
    @rtype: Dataframe
    usage:
    tweet = {
      "id": "1",
     "text": "I am scoring some points in tonight's game"}
    tweets = [tweet]
    tweetAnalyzer = sentiment_analysis(tweets)
    """
    client = _authenticate(_key,_endpoint)
    response = client.analyze_sentiment(documents=tweet)[0]
    tweetdf =_formatresponse(response)
    return tweetdf

