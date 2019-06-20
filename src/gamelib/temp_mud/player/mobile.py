from ..errors import CommandError
from .base_player import BasePlayer


SCALES = {
    1: 2,
    2: 3,
    3: 3,
    4: 4,
    5: 4,
    6: 5,
    7: 6,
}


def scale():
    return SCALES.get(len([player for player in MOBILES if player.exists]), 7)


class Mobile(BasePlayer):
    def __init__(self, player_id):
        self.player_id = player_id
        self.__name = None
        self.__location_id = None
        self.__strength = None
        self.__sex = None
        self.__weapon = None
        self.__visible = 0
        self.__level = None

    # Reset data
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def location(self):
        return Location(self.__location_id)

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, value):
        self.__strength = value

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, value):
        self.__sex = value

    @property
    def level(self):
        return self.__level

    @classmethod
    def reset_players(cls):
        for mobile in MOBILES:
            mobile.reset()
        for player in Player.players()[16 + len(MOBILES):]:
            player.reset()

    # Other
    def attack(self, enemy):
        if self.location.location_id != enemy.location.location_id:
            return
        if not 0 <= self.player_id <= 47:
            return
        chance = randperc()
        defense = 3 * (15 - enemy.level) + 20

        shields = [Item(89), Item(113), Item(114)]
        if any(shield.is_worn_by(enemy) for shield in shields):
            defense -= 10

        if chance < defense:
            damage = randperc() * self.damof
        else:
            damage = -1

        self.send_message(
            enemy,
            self,
            -10021,
            self.location,
            [self.player_id, damage, None],
        )

    def get_damage(self, enemy, damage):
        self.strength -= damage

        if self.strength >= 0:
            return self.attack(enemy)

        self.dump_items()
        self.send_global("{} has just died\n".format(self.name))
        self.remove()
        self.send_wizard("[ {} has just died ]\n".format(self.name))

    def get_lightning(self, enemy):
        if self.is_mobile:
            # DIE
            self.get_damage(enemy, 10000)

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

    def on_steal(self, actor):
        if self.is_mobile:
            self.get_damage(actor, 0)

    # Abstract
    @property
    def position(self):
        raise NotImplementedError()

    @property
    def visible(self):
        raise NotImplementedError()

    @property
    def weapon(self):
        raise NotImplementedError()

    @property
    def helping(self):
        raise NotImplementedError()

    @property
    def sex(self):
        raise NotImplementedError()

    @property
    def exists(self):
        raise NotImplementedError()

    @property
    def is_mobile(self):
        raise NotImplementedError()

    def woundmn(self, *args):
        raise NotImplementedError()

    def check_kicked(self):
        raise NotImplementedError()


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
