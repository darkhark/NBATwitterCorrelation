from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from pandas import DataFrame


def getPlayerSeasonalGameStats(fullName: str, year: int) -> DataFrame.__class__:
    """
    Retrieve a player's seasonal stats from the nba_api. Each row will be one game in the
    season and each column is a different statistic.

    :param fullName: The first and last name of the player player separated by a space
    :param year: The year for the season when the data should be obtained.
    :return: A pandas dataframe containing box summary stats for a single player's season
    """
    playerID = _getPlayerID(fullName)
    return _getPlayerStats(playerID, year)


def _getPlayerID(fullName: str) -> str:
    player_dict = players.get_players()
    player = [player for player in player_dict if player['full_name'] == fullName][0]
    return player['id']


def _getPlayerStats(playerID: str, year: int) -> DataFrame.__class__:
    gamelog = playergamelog.PlayerGameLog(player_id=playerID, season=str(year))
    return gamelog.get_data_frames()[0]
