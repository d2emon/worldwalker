from games.mud.exceptions import FileServiceError
from .world import WorldService
from .world.player import Player


def post(username, channel_id):
    WorldService.connect()

    if Player.fpbn(username) is not None:
        raise FileServiceError("You are already on the system - you may only be on once at a time")

    return Player.put_on(username, channel_id)


def put_event_id(player_id, event_id):
    WorldService.connect()
    Player.players[player_id].position = event_id
