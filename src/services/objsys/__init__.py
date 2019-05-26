from ..world.player import Player


class ObjectsServices:
    @classmethod
    def fpbn(cls, name):
        player_id = cls.fpbns(name)
        # if new1.ail_blind:
        #     return None
        if player_id is None:
            return None
        # if player_id == Talker.player_id:
        #     return player_id
        # if not Talker.see_player(player_id):
        #     return None

        return player_id

    @classmethod
    def fpbns(cls, name):
        """

        :param name:
        :return:
        """
        n1 = name.lower()
        for a in range(48):
            player = Player.players[a]
            n2 = player.name.lower()
            if not n2:
                continue
            if n1 == n2:
                return player
            if n2[:4] == "the " and n1 == n2[4:]:
                return player
        return None
