from ..errors import CommandError


class Mobile:
    def __init__(self, player_id):
        self.player_id = player_id

    @property
    def exists(self):
        raise NotImplementedError()

    @property
    def is_mobile(self):
        raise NotImplementedError()

    @property
    def location(self):
        raise NotImplementedError()

    def woundmn(self, *args):
        raise NotImplementedError()

    def is_here(self, player):
        if not self.exists:
            return
        if player.location is None:
            return False
        return player.location.location_id == self.location.location_id

    def on_actor_enter(self, actor, direction, location):
        if not self.is_here(actor):
            return
        pass

    def on_actor_leave(self, actor, direction):
        if not self.is_here(actor):
            return
        pass

    def on_steal(self):
        if self.is_mobile:
            self.woundmn(0)


class Golem(Mobile):
    def __init__(self):
        super().__init__(25)

    def on_actor_leave(self, actor, direction):
        if not self.is_here(actor):
            return

        if MagicSword().is_carried_by(actor):
            raise CommandError("\001cThe Golem\001 bars the doorway!\n")


class Figure(Mobile):
    def on_actor_enter(self, actor, direction, location):
        # super().on_actor_enter(actor, direction_id, location_id)

        figure = Player.find("figure")
        if not figure.is_here(actor):
            return
        if actor == figure:
            return
        if direction.direction_id != 2:
            return

        sorcerors = Item101(), Item102(), Item103()
        if any(item.iswornby(actor) for item in sorcerors):
            raise CommandError("\001pThe Figure\001 holds you back\n"
                               "\001pThe Figure\001 says 'Only true sorcerors may pass'\n")


MOBILES = [
    Golem(),  # 25

    Figure(),
]
