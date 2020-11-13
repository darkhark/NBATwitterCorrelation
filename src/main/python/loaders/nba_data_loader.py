import json
from pathlib import Path

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
    playerID = __getPlayerID(fullName)
    return __getPlayerStats(playerID, year)


def __getPlayerID(fullName: str) -> str:
    player_dict = players.get_players()
    player = None
    for person in player_dict:
        if person['full_name'] == fullName:
            print('Name matched!')
            player = person
    assert (player is not None), 'Player name does not exist!'
    return player['id']


def __getPlayerStats(playerID: str, year: int) -> DataFrame.__class__:
    gamelog = playergamelog.PlayerGameLog(player_id=playerID, season=str(year))
    return gamelog.get_data_frames()[0]


def getNBASeasonRanges():
    """
    @return: A dictionary where the key is the year and the value is the start and end dates
    of that season.
    @rtype: dictionary
    """
    location = str(Path(__file__).parent.parent.parent.parent.parent / "docs") + "/Data/nba_season_ranges.json"
    with open(location, 'r') as json_file:
        years = json.load(json_file)
    return years
