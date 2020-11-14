from datetime import datetime

# import loaders.nba_data_loader as ndl
# import pandas as pd


def cleanNBAData(df):
    cleanDF = df[['GAME_DATE', 'PTS', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA']].copy()  # double brackets for columns
    cleanDF['GAME_DATE'] = cleanDF['GAME_DATE'].map(lambda date: date.replace(',', ''))\
        .map(lambda date: datetime.strptime(date, '%b %d %Y'))
    cleanDF = getAverageAndAccuracyPlusMinus(cleanDF)
    return cleanDF


def getAverageAndAccuracyPlusMinus(df):
    numRows = len(df.index)
    avgDF, avgPoints = getPlusMinusPoints(df, numRows)
    avgDF, avgAcc = getPlusMinusAcc(avgDF, numRows)
    avgDF = avgDF.drop(
        ['PTS', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
         'ShotsMade', 'ShotsAttempted', 'PlayerAvg', 'GameAcc', 'accAvg'],
        axis=1)
    return avgDF, avgPoints, avgAcc


def getPlusMinusPoints(df, numRows):
    pointsDF = df.copy()
    pointsDF['PlayerAvg'] = pointsDF['PTS'].sum() / numRows
    pointsDF['PlusMinusPoints'] = pointsDF['PTS'] - pointsDF['PlayerAvg']
    avg = pointsDF['PlayerAvg'][0]
    return pointsDF, avg


def getPlusMinusAcc(df, numRows):
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

