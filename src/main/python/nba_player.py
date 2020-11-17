import loaders.twitter_handle_loader as thl
import loaders.nba_data_loader as ndl
import loaders.twitter_data_loader as tdl
import cleansers.twitter_data_cleaner as tdc
import cleansers.nba_data_cleanser as ndc

import pandas as pd
import datetime


class NBAPlayer:
    allPlayers = {}

    def __new__(cls, name, *args, **kwargs):
        """
        Only used for cache maintenance. Called before init.
        The super in here I believe refers to __init__
        """
        if name in cls.allPlayers.keys():
            return cls.allPlayers[name]
        player = super(NBAPlayer, cls).__new__(cls)
        return player

    def __init__(self, name: str):
        """
        Creates the NBAPlayer object.

        @param name: The player's first and last name as a single string with correct capitalization.
        @type name: str
        """
        if name in NBAPlayer.allPlayers.keys():
            return
        self.name = name
        self.handle = thl.getTwitterHandle(self.name)
        self.plusMinus, self.avgPoints, self.avgAcc = self.getEverySeasonStats()
        self.tweets = self.getEverySeasonTweets()
        NBAPlayer.allPlayers[name] = self

    def getEverySeasonStats(self):
        """
        @param name: The player's name.
        @return: A dictionary where the key is the year and the value is dataframe for
        all the stats in that year.
        @rtype: dictionary
        """
        statDict = {}
        avgPointsDict = {}
        avgAccDict = {}
        for year in ndl.getNBASeasonRanges():
            dirtyStats = ndl.getPlayerSeasonalGameStats(self.name, int(year))
            statDict[year], avgPointsDict[year], avgAccDict[year] = ndc.cleanNBAData(dirtyStats)
        return statDict, avgPointsDict, avgAccDict

    def getEverySeasonTweets(self):
        """
        @return: A dictionary where the key is the year and the value is a dataframe for
        all the tweets in that year.
        @rtype: dictionary
        """
        tweetsDict = {}
        allSeasons = ndl.getNBASeasonRanges()
        for year in allSeasons:
            dateRange = allSeasons[year]
            startDate = dateRange[0]
            endDate = dateRange[1]
            dirtyTweets = tdl.getPlayerTweetsAsDF(self.handle, startDate, endDate)
            tweetsDict[year] = tdc.cleanTweets(dirtyTweets)
        return tweetsDict

    def getAllStatsAndTweetsDF(self):
        """
        Merges the tweets and stats data for every year for this player.
        @return: A dataframe for all of this players tweets and plusminus stats from 2015 - 2019.
        The df is indexed on tweet ids and the columns are TweetDate (The date of a game),
        Tweet (All tweets leading into a game merged into one), PlusMinusPoints (The amount above or below the player's
        season average scored in this game), and PlusMinusAcc (The percent above or below the player's average accuracy for
        that season
        @rtype: Dataframe
        """
        bigDF = pd.DataFrame()
        for year in self.plusMinus.keys():
            if bigDF.empty:
                bigDF = self.getStatsAndTweetsDFPerYear(year)
            else:
                df = self.getStatsAndTweetsDFPerYear(year)
                if not df.empty:
                    bigDF = bigDF.append(df)
        return bigDF

    def getStatsAndTweetsDFPerYear(self, year):
        """
        Merges the stats and tweets DFs for the given year

        @param year: The NBA season to merge the DFs for.
        @return: A dataframe for all of this players tweets and plusminus stats for the given year.
        The df is indexed on tweet ids and the columns are TweetDate (The date of a game),
        Tweet (All tweets leading into a game merged into one), PlusMinusPoints (The amount above or below the player's
        season average scored in this game), and PlusMinusAcc (The percent above or below the player's average accuracy for
        that season
        @rtype: Dataframe
        """
        year = str(year)
        statsDF = self.plusMinus[year]
        gameDates = statsDF['GAME_DATE'].tolist()
        combinedTweetsDF = self.__combineTweetsPerGame(gameDates, year)
        mergedDF = pd.merge(
            left=combinedTweetsDF,
            right=statsDF,
            left_on='TweetDate',
            right_on='GAME_DATE',
            how='outer'
        ).dropna().set_index(combinedTweetsDF.index)
        mergedDF.drop('GAME_DATE', axis=1, inplace=True)
        return mergedDF

    def __combineTweetsPerGame(self, gameDates, year):
        tweetsDF = self.tweets[year]
        combinedTweetsDF = pd.DataFrame()
        previousGameDate = None
        for gameDate in gameDates:
            if combinedTweetsDF.empty:
                combinedTweetsDF = tweetsDF.loc[tweetsDF['TweetDate'] <= gameDate]
                if not combinedTweetsDF.empty:
                    combinedTweetsDF = self.__squishTweets(combinedTweetsDF, gameDate)
            else:
                weekPrevious = gameDate - datetime.timedelta(days=7)
                if weekPrevious < previousGameDate:
                    betweenGamesDF = tweetsDF.loc[(previousGameDate < tweetsDF['TweetDate'])
                                                  & (tweetsDF['TweetDate'] <= gameDate)]
                else:
                    betweenGamesDF = tweetsDF.loc[(weekPrevious < tweetsDF['TweetDate'])
                                                  & (tweetsDF['TweetDate'] <= gameDate)]
                if not betweenGamesDF.empty:
                    betweenGamesDF = self.__squishTweets(betweenGamesDF, gameDate)
                    combinedTweetsDF = combinedTweetsDF.append(betweenGamesDF)
            previousGameDate = gameDate
        return combinedTweetsDF

    def __squishTweets(self, df, gameDate):
        allTweetsInOne = ""
        for tweet in df['Tweet']:
            allTweetsInOne += tweet
        lastIndex = df.index.values[-1]
        df.loc[lastIndex]['Tweet'] = allTweetsInOne
        df.loc[lastIndex]['TweetDate'] = gameDate
        return df.tail(1)


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)
# Test Code - cache works
# lebron = NBAPlayer('LeBron James')
# print(lebron.name, ":", lebron.handle)
# print(NBAPlayer.allPlayers)
# lebron2 = NBAPlayer('LeBron James')
# print(NBAPlayer.allPlayers)
# harden = NBAPlayer('James Harden')
# print(NBAPlayer.allPlayers)

# Test Code - view stats and tweets separate
# lebron = NBAPlayer('LeBron James')
# print(NBAPlayer.allPlayers[lebron.name].plusMinus['2018'])
# print(NBAPlayer.allPlayers[lebron.name].tweets['2018'])

# Test Code - merge tweets and stats
# lebron = NBAPlayer("Kyle Lowry")
# print(lebron.getAllStatsAndTweetsDF())
