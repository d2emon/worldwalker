from games.mud.exceptions import FileServiceError
from .file_services import LogFile
from .world import WorldService
from .world.player import Player


class MudExeServices:
    @classmethod
    def post_log(cls, message):
        LogFile.log(message)

    @classmethod
    def post_player(cls, username, channel):
        try:
            WorldService.connect()
        except FileServiceError:
            raise FileServiceError("Sorry AberMUD is currently unavailable")

        if Player.fpbn(username) is not None:
            raise FileServiceError("You are already on the system - you may only be on once at a time")

        return Player.put_on(username, channel)

    @classmethod
    def get_messages(cls, message_id=None):
        try:
            WorldService.connect()
            last_message = WorldService.get_last_message_id()
            first_message = message_id or last_message
            messages = [WorldService.get_message(i) for i in range(first_message, last_message)]
            return {
                'message_id': message_id,
                'messages': messages,
            }
        except FileServiceError:
            raise FileServiceError("AberMUD: FILE_ACCESS : Access failed\n")

    @classmethod
    def put_position(cls, player_id, message_id):
        WorldService.connect()
        Player.players[player_id].position = message_id
