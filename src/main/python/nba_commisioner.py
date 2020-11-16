import loaders.twitter_handle_loader as thl
from nba_player import NBAPlayer

import pandas as pd


def getAllStatsAndTweetsAllPlayers():
    allTweetsAndStatsDF = pd.DataFrame()
    for name in thl.getAllTwitterHandles().keys():
        print(name)
        errorPlayers = ['Devin Booker', 'Trae Young', 'Luka Doncic', 'Donovan Mitchell', 'Jayson Tatum', 'Kevin Durant',
                        'Joel Embiid', 'DeMarcus Cousins', 'Klay Thompson']
        if name not in errorPlayers:
            player = NBAPlayer(name)
            playerTweetsAndStats = player.getAllStatsAndTweetsDF()
            if allTweetsAndStatsDF.empty:
                allTweetsAndStatsDF = playerTweetsAndStats
            else:
                allTweetsAndStatsDF = allTweetsAndStatsDF.append(playerTweetsAndStats)
    return allTweetsAndStatsDF


# Test Code
# print(getAllStatsAndTweetsAllPlayers())
