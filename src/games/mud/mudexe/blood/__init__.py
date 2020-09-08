from services.world import WorldService


class Blood:
    fighting = None
    in_fight = None
    wpnheld = None

    @classmethod
    def fighting_with(cls):
        return WorldService.get_player(cls.fighting)

    @classmethod
    def stop_fight(cls):
        cls.in_fight = 0
        cls.fighting = None

    @classmethod
    def __clean_fight(cls, channel):
        if not cls.fighting_with().exists:
            cls.stop_fight()
        if cls.fighting_with().location != channel:
            cls.stop_fight()

    @classmethod
    def update(cls, channel):
        if cls.fighting is not None:
            cls.__clean_fight(channel)
        if cls.in_fight:
            cls.in_fight -= 1

    @classmethod
    def next_turn(cls, channel, interrupt):
        if not cls.in_fight:
            return
        cls.__clean_fight(channel)
        if cls.in_fight:
            if interrupt:
                cls.in_fight = 0
                # hitplayer(cls.fighting, cls.wpnheld)
