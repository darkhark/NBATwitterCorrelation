import json


def getAllTwitterHandles():
    """
    Returns the top 15 point scorers over the last 5 NBA seasons.

    @return: A dictionary where the keys are the player names and the values are
    the players' Twitter handles
    @rtype: dict
    """
    with open('docs/Data/twitter_handles.json') as json_file:
        twitter_handles = json.load(json_file)
    return twitter_handles


def getTwitterHandle(name: str):
    """
    Finds the player's handle for the name provided.

    @param name: The player's first and last name as a single string with correct capitalization.
    @type name: string
    @return: The twitter handle for that player
    @rtype: str
    """
    playerDict = getAllTwitterHandles()
    return playerDict[name]
