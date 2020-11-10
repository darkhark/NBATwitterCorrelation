import snscrape.modules.twitter as sntwitter


def getPlayerTweets(handle: str, since: str, until: str) -> dict:
    """

    :param handle: handle of player whose tweet IDs are being retrieved
    :param since: string indicating the lower bound date
    :param until: string indicating the upper bound date
    :return: dict with tweet id as key, tweet object as value
    """
    return {tweet.id: tweet for i, tweet in
            enumerate(sntwitter.TwitterSearchScraper('from:%s since:%s until:%s' % (handle, since, until)).get_items())}
