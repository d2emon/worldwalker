import random
from ..errors import ServiceError
from .world import WorldService


class PlayerData:
    def __init__(self, player_id):
        self.player_id = player_id
        self.name = None
        # 2
        # 3

        self.location = None
        self.message_id = -1
        # 6
        self.strength = -1

        self.visible = 0
        self.sex = 0
        self.level = 1
        self.weapon = None

    @property
    def exists(self):
        return self.name is not None

    @classmethod
    def __start_location(self):
        return random.choice((-5, -183))

    def equal(self, search):
        if not self.exists:
            return False

        name = self.name.lower()
        names = [name]
        if name[:4] == "the ":
            names.append(name[4:])
        return search in names

    def serialize(self):
        return [
            self.player_id,
            self.name,
            None,
            None,

            self.location if self.location is not None else self.__start_location(),
            self.message_id,
            None,
            self.strength,

            self.visible,
            self.sex,
            self.level,
            self.weapon,

            None,
            None,
            None,
            None,
        ]


class PlayersService:
    __players_count = 48
    __players = [PlayerData(player_id) for player_id in range(__players_count)]

    @classmethod
    def __get_player_id(cls, **kwargs):
        player_id = kwargs.get('player_id')
        if not 0 <= player_id < cls.__players_count:
            raise ServiceError("No player with this player id")
        return player_id

    @classmethod
    def get_info(cls, **kwargs):
        player_id = cls.__get_player_id(**kwargs)
        player = next((player for player in cls.__players if player.player_id == player_id), None)
        if player is None:
            raise ServiceError("No player with this player id")
        return player.serialize()

    # Tk
    @classmethod
    def get_new_player(cls, **kwargs):
        if len(PlayersService.get_players(**kwargs)) > 0:
            raise ServiceError("You are already on the system - you may only be on once at a time")

        player = next((player for player in cls.__players if not player.exists), None)
        if player is None:
            raise ServiceError("\nSorry AberMUD is full at the moment\n")
        player.name = kwargs.get('name', '')
        return player.serialize()

    @classmethod
    def get_new_player_id(cls):
        return next((player.player_id for player in cls.__players if not player.exists), None)

    @classmethod
    def get_players_count(cls):
        return cls.__players_count

    # ObjSys
    @classmethod
    def get_players(cls, **kwargs):
        name = kwargs.get('name', '').lower()
        return [player.player_id for player in cls.__players if player.equal(name)]
