from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from pandas import DataFrame


class NBADataLoader:

    @staticmethod
    def getPlayerSeasonalBoxData(fullName: str, year: int) -> DataFrame.__class__:
        """
        Retrieve a player's seasonal data from the nba_api based on their season

        :param fullName: The first and last name of the player player separated by a space
        :param year: The year for the season when the data should be obtained.
        :return: A pandas dataframe containing box summary stats for a single player's season
        """
        playerID = NBADataLoader._getPlayerID(fullName)
        return NBADataLoader._getPlayerStats(playerID, year)

    @staticmethod
    def _getPlayerID(fullName: str) -> str:
        player_dict = players.get_players()
        player = [player for player in player_dict if player['full_name'] == fullName][0]
        return player['id']

    @staticmethod
    def _getPlayerStats(playerID: str, year: int) -> DataFrame.__class__:
        gamelog = playergamelog.PlayerGameLog(player_id=playerID, season=str(year))
        return gamelog.get_data_frames()[0]
