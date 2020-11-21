from pandas import DataFrame
import snscrape.modules.twitter as sntwitter


def getPlayerTweets(handle: str, since: str, until: str) -> dict:
    """
    Retrieves player tweets within the specified time period.

    :param handle: handle of player whose tweet IDs are being retrieved
    :param since: string indicating the lower bound date
    :param until: string indicating the upper bound date
    :return: dict with tweet id as key, tweet object as value
    """
    return {tweet.id: tweet for i, tweet in
            enumerate(sntwitter.TwitterSearchScraper('from:%s since:%s until:%s' % (handle, since, until)).get_items())}


def getPlayerTweetsAsDF(handle: str, since: str, until: str) -> DataFrame.__class__:
    tweetObjectsDict = getPlayerTweets(handle, since, until)
    tweetsDict = __getTweetsDatesAndIDsOnly(tweetObjectsDict)
    return DataFrame.from_dict(tweetsDict, orient='index', columns=['TweetDate', 'Tweet']).sort_values('TweetDate')


def __getTweetsDatesAndIDsOnly(tweetsObjectDict: dict) -> dict:
    brokenDownDict = {}
    for key in tweetsObjectDict:
        tweetObj = tweetsObjectDict[key]
        brokenDownDict[key] = [tweetObj.date, tweetObj.content]
    return brokenDownDict
