from ..database.world import World


class TkGlobals:
    __user = None

    # oddcat = 0
    # talkfl = 0

    curmode = 0
    # meall = 0

    # gurum = 0
    convflg = 0

    rd_qd = 0

    # dsdb = 0;
    # moni = 0;

    # bound = 0
    # tmpimu = 0
    # echoback = "*e"
    # tmpwiz = "."  # Illegal name so natural immunes are ungettable!

    @classmethod
    def set_user(cls, user):
        cls.__user = user

    @classmethod
    def cms(cls):
        return cls.__user.message_id

    @classmethod
    def iamon(cls):
        return cls.__user.is_on

    @classmethod
    def mynum(cls):
        return cls.__user.person_id

    @classmethod
    def curch(cls):
        return cls.__user.location_id

    @classmethod
    def globme(cls):
        return cls.__user.name

    @classmethod
    def fl_com(cls):
        return World.database

    @classmethod
    def lasup(cls):
        return cls.__user.last_update

    @classmethod
    def i_setup(cls):
        return cls.__user.in_setup
