class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def location(self):
        raise NotImplementedError()

    @property
    def is_alive(self):
        return bool(self.name)

    @property
    def is_mobile(self):
        return self.player_id >= 16

    @classmethod
    def fpbn(cls, player_name, not_found_error=None):
        raise NotImplementedError()
