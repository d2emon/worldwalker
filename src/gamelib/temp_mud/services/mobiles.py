from ..errors import ServiceError
from ..item.item import Item


class MobilesService:
    __mobiles = [
        # 0-15
        ["The Wraith", -1077, 60, 0, -2],
        ["Shazareth", -1080, 99, 0, -30],
        ["Bomber", -308, 50, 0, -10],
        ["Owin", -311, 50, 0, -11],
        ["Glowin", -318, 50, 0, -12],

        ["Smythe", -320, 50, 0, -13],
        ["Dio", -332, 50, 0, -14],
        ["The Dragon", -326, 500, 0, -2],
        ["The Zombie", -639, 20, 0, -2],
        ["The Golem", -1056, 90, 0, -2],
        ["The Haggis", -341, 50, 0, -2],
        ["The Piper", -630, 50, 0, -2],
        ["The Rat", -1064, 20, 0, -2],
        ["The Ghoul", -129, 40, 0, -2],
        ["The Figure", -130, 90, 0, -2],

        ["The Ogre", -144, 40, 0, -2],
        ["Riatha", -165, 50, 0, -31],
        ["The Yeti", -173, 80, 0, -2],
        ["The Guardian", -197, 50, 0, -2],
        ["Prave", -201, 60, 0, -400],
        ["Wraith", -350, 60, 0, -2],
        ["Bath", -1, 70, 0, -401],
        ["Ronnie", -809, 40, 0, -402],
        ["The Mary", -1, 50, 0, -403],
        ["The Cookie", -126, 70, 0, -404],

        ["MSDOS", -1, 50, 0, -405],
        ["The Devil", -1, 70, 0, -2],
        ["The Copper", -1, 40, 0, -2],
    ]
    __default = ["", 0, 0, 0, 0]

    @classmethod
    def __as_dict(cls, mobile):
        return {
            'name': mobile[0],
            'location_id': mobile[1],
            'strength': mobile[2],
            'sex': mobile[3],
            'weapon': None,
            'visible': 0,
            'level': mobile[4],
        }

    @classmethod
    def get(cls, **kwargs):
        player_id = kwargs.get('player_id')
        if player_id is None:
            return [cls.__as_dict(player) for player in cls.__mobiles]
        player_id -= 16
        if player_id < 0 or player_id > len(cls.__mobiles):
            return cls.__as_dict(cls.__default)
        return cls.__as_dict(cls.__mobiles[player_id])
