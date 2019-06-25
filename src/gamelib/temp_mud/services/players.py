from ..errors import ServiceError
from .world import WorldService


class PlayersService:
    __players_count = 196
    __players = []

    @classmethod
    def __get_player_id(cls, **kwargs):
        player_id = kwargs.get('player_id')
        if not 0 <= player_id < cls.__players_count:
            raise ServiceError("No player with this player id")
        return player_id

    @classmethod
    def get_info(cls, **kwargs):
        player_id = cls.__get_player_id(**kwargs)
        return WorldService.get_player(player_id=player_id)

    @classmethod
    def get_players_count(cls):
        return cls.__players_count
