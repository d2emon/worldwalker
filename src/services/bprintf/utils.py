from ..weather import WeatherServices
from ..world.player import Player


class Parser:
    wd_it = None
    wd_him = None
    wd_her = None
    wd_them = None

    @classmethod
    def set_name(cls, player):
        if player.player_id > 15 and player.player_id not in [fpnbs("riatha"), fpbns("shazareth")]:
            cls.wd_it = player.name
            return

        if player.sex:
            cls.wd_her = player.name
        else:
            cls.wd_him = player.name
        cls.wd_them = player.name


class User:
    def __init__(self):
        self.player_id = None
        self.channel = None

    @property
    def player(self):
        return Player.players[self.player_id]

    def see_player(self, player):
        if player.player_id is None:
            return True

        if player.player_id == self.player_id:
            return True

        if self.player.level < player.visible:
            return False

        if self.channel != player.location:
            return True

        return WeatherServices.get_is_dark(self.channel)


def seeplayer(player_id, user=None, new1=None):
    if new1.ail_blind:
        # Cant see
        return False

    if player_id is None:
        return True

    if player_id == user.player_id:
        return True

    player = Player.players[player_id]
    if user.see_player(player):
        Parser.set_name(player)
        return True
    else:
        return False


def see_player(player_id, user):
    player = Player.players[player_id]
    return user.see_player(player)
