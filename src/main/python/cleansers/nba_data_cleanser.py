from datetime import datetime
import pandas as pd
# import loaders.nba_data_loader as ndl


def cleanNBAData(df: pd.DataFrame.__class__):
    """
    Removes stats not beneficial to the analysis while creating new columns that fit closer to our main goal.

    @param df: The dataframe to clean. Should come from nba_data_loader
    @return: A dataframe consisting of GAME_DATE, PlusMinusPoints, and PlusMinusAcc. The plus minus column values
    are positive if they're above average and negative otherwise.
    @rtype: Dataframe
    """
    cleanDF = df[['GAME_DATE', 'PTS', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA']].copy()  # double brackets for columns
    cleanDF['GAME_DATE'] = cleanDF['GAME_DATE'].map(lambda date: date.replace(',', ''))\
        .map(lambda date: datetime.strptime(date, '%b %d %Y').date())
    cleanDF, avgPoints, avgAcc = __getAverageAndAccuracyPlusMinus(cleanDF)
    cleanDF = cleanDF.sort_values('GAME_DATE')
    return cleanDF, avgPoints, avgAcc


def __getAverageAndAccuracyPlusMinus(df):
    numRows = len(df.index)
    avgDF, avgPoints = __getPlusMinusPoints(df, numRows)
    avgDF, avgAcc = __getPlusMinusAcc(avgDF, numRows)
    avgDF = avgDF.drop(
        ['PTS', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
         'ShotsMade', 'ShotsAttempted', 'PlayerAvg', 'GameAcc', 'accAvg'],
        axis=1)
    return avgDF, avgPoints, avgAcc


def __getPlusMinusPoints(df, numRows):
    pointsDF = df.copy()
    pointsDF['PlayerAvg'] = pointsDF['PTS'].sum() / numRows
    pointsDF['PlusMinusPoints'] = pointsDF['PTS'] - pointsDF['PlayerAvg']
    avg = pointsDF['PlayerAvg'][0]
    return pointsDF, avg


def __getPlusMinusAcc(df, numRows):
    accDF = df.copy()
    accDF['ShotsMade'] = accDF['FGM'] + accDF['FG3M'] + accDF['FTM']
    accDF['ShotsAttempted'] = accDF['FGA'] + accDF['FG3A'] + accDF['FTA']
    accDF['GameAcc'] = accDF['ShotsMade'] / accDF['ShotsAttempted']
    accDF['accAvg'] = accDF['GameAcc'].sum() / numRows
    accDF['PlusMinusAcc'] = accDF['GameAcc'] - accDF['accAvg']
    avgAcc = accDF['accAvg'][0]
    return accDF, avgAcc


# pd.set_option('display.max_columns', None)
# dfnba = ndl.getPlayerSeasonalGameStats('LeBron James', 2019)
# dfnba, average, avgAccuracy = cleanNBAData(dfnba)
# print(dfnba)
# print(average)
# print(avgAccuracy)

