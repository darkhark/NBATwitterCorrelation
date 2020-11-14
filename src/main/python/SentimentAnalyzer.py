from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def sentiment_analysis(tweet):
    # Authentication
    key = "adc96f39ac2a4918a1f462b5bf8674b8"
    endpoint = "https://nbatwittersentiment.cognitiveservices.azure.com/"
    ta_credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential,
        api_version='TextAnalyticsApiVersion.V3_0')
    response = client.analyze_sentiment(documents=tweet)[0]
    return response.sentences
    # print("Document Sentiment: {}".format(response.sentiment))
    # print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
    #     response.confidence_scores.positive,
    #     response.confidence_scores.neutral,
    #     response.confidence_scores.negative,
    # ))
    # for idx, sentence in enumerate(response.sentences):
    #     print("Sentence: {}".format(sentence.text))
    #     print("Sentence {} sentiment: {}".format(idx + 1, sentence.sentiment))
    #     print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
    #         sentence.confidence_scores.positive,
    #         sentence.confidence_scores.neutral,
    #         sentence.confidence_scores.negative,
    #     ))


tweet1 = {
    "language": "en",
    "id": "1",
    "text": "Hello world This is some input text that I love."
}

tweets = [tweet1]
tweetAnalyzer = sentiment_analysis(tweets)
for x in tweetAnalyzer:
    print(x)
