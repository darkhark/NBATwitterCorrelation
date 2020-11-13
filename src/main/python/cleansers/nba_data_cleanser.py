from datetime import datetime

import loaders.nba_data_loader as ndl
import pandas as pd


def cleanNBAData(df):
    cleanDF = df[['GAME_DATE', 'PTS', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA']]  # double brackets for columns
    cleanDF['GAME_DATE'] = cleanDF['GAME_DATE'].map(lambda date: date.replace(',', ''))\
        .map(lambda date: datetime.strptime(date, '%b %d %Y'))
    return cleanDF


pd.set_option('display.max_columns', None)
dfnba = ndl.getPlayerSeasonalGameStats('LeBron James', 2019)
dfnba = cleanNBAData(dfnba)
print(dfnba)

