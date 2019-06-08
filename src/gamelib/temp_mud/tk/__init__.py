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
from ..player import Player
from ..syslog import syslog


def split(block, name):
    name = name.lower()
    name1, name2 = block[2].split(".")
    # wkblock = block[2:126]
    # work = block[64:64]
    is_me = name1.lower() == name
    if name1[:4].lower() == "the ":
        if name1[4:].lower() == name:
            is_me = True
    return is_me, name1, name2, block[64]


def userwrap(user):
    if Player.fpbns(user.name) is None:
        return
    user.loose()
    syslog(user, "System Wrapup exorcised {}".format(user.name))
