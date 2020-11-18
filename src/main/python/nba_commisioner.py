from pathlib import Path

import loaders.twitter_handle_loader as thl
from nba_player import NBAPlayer
import os
import pandas as pd


picklePath = str(Path(__file__).parent.parent.parent.parent / "docs") + "/Data/allStatsAndTweets.pkl"


def getAllStatsAndTweetsAllPlayers(updatePickle=False):
    allTweetsAndStatsDF = pd.DataFrame()
    print("Loading players...")
    if os.path.isfile(picklePath) and not updatePickle:
        pd.read_pickle(picklePath)
    else:
        for name in thl.getAllTwitterHandles().keys():
            print('Loaded', name + "'s", 'tweets and stats.')
            errorPlayers = ['Devin Booker', 'Trae Young', 'Luka Doncic', 'Donovan Mitchell', 'Jayson Tatum', 'Kevin Durant',
                            'Joel Embiid', 'DeMarcus Cousins', 'Klay Thompson']
            if name not in errorPlayers:
                player = NBAPlayer(name)
                playerTweetsAndStats = player.getAllStatsAndTweetsDF()
                if allTweetsAndStatsDF.empty:
                    allTweetsAndStatsDF = playerTweetsAndStats
                else:
                    allTweetsAndStatsDF = allTweetsAndStatsDF.append(playerTweetsAndStats)
        allTweetsAndStatsDF.to_pickle(picklePath)
    return allTweetsAndStatsDF


def getAllTweetsAllPlayersAsDict():
    """
    Needs to be ran after getAllStatsAndTweetsAllPlayers. Collects all the tweets from
    every player and returns it as a single dictionary.
    @return: A dictionary of tweetID: tweet
    @rtype: Dictionary
    """
    tweetDict = dict()
    for player in NBAPlayer.allPlayers.values():
        tweetDict.update(player.getAllTweetsAsDict())
    return tweetDict


# Test Code
# print(getAllStatsAndTweetsAllPlayers(), "------------------------------------------------------------")
# print(getAllTweetsAllPlayersAsDict())
