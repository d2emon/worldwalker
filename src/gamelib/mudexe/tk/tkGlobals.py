class TkGlobals:
    __user = None

    i_setup = 0
    # oddcat = 0
    # talkfl = 0

    curmode = 0
    # meall = 0

    # gurum = 0
    convflg = 0

    fl_com = None

    rd_qd = 0

    # dsdb = 0;
    # moni = 0;

    # bound = 0
    # tmpimu = 0
    # echoback = "*e"
    # tmpwiz = "."  # Illegal name so natural immunes are ungettable!

    lasup = 0

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
