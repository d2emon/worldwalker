"""
AberMUD II   C

This game systems, its code scenario and design
are (C) 1987/88  Alan Cox,Jim Finnis,Richard Acott

This file holds the basic communications routines
"""

"""
Data format for mud packets
 
Sector 0
[64 words]
0   Current first message pointer
1   Control Word
Sectors 1-n  in pairs ie [128 words]
 
[channel][controlword][text data]
 
[controlword]
0 = Text
- 1 = general request
"""
from ..action import Special
from ..message import MSG_WIZARD, MSG_GLOBAL
from ..player import Player
from ..syslog import syslog
from ..world import World


def split(block, luser):
    name1, name2 = block[2].split(".")
    if name1[:4].lower() == "the ":
        if name1[4:].lower() == luser.lower():
            return True, name1, name2, block[64]
    return name1.lower() == luser.lower(), name1, name2, block[64]


def userwrap(user):
    if Player.fpbns(user.name) is None:
        return
    user.loose()
    syslog(user, "System Wrapup exorcised {}".format(user.name))


class StartGame(Special):
    @classmethod
    def action(cls, parser, user):
        parser.mode = parser.MODE_GAME

        user.reset_location_id()
        user.initme()

        World.load()
        visible = 0 if not user.is_god else 10000
        user.player.start(user.NewUaf.strength, user.NewUaf.level, visible, user.NewUaf.sex)

        user.send_message(
            user,
            MSG_WIZARD,
            user.location_id,
            "\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=user),
        )

        yield from parser.read_messages()
        user.reset_location_id(True)
        user.go_to_channel(user.location_id)

        user.send_message(
            user,
            MSG_GLOBAL,
            user.location_id,
            "\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=user),
        )
