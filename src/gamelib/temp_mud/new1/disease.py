from ..errors import CommandError
from ..bprintf import bprintf
from ..newuaf import NewUaf
from ..parse import gamecom


class Disease:
    error_message = ""
    activate_message = ""

    def __init__(self, active=False):
        self.__active = active

    @property
    def active(self):
        return self.__active

    def activate(self):
        self.__active = False

    def cure(self):
        self.__active = False

    def check(self):
        if self.active:
            raise CommandError(self.error_message)

    def magic(self, caster):
        if NewUaf.my_lev < 10:
            bprintf(self.activate_message)
            self.activate()
        else:
            bprintf("\001p{}\001 tried to dumb you\n".format(caster))


class Dumb(Disease):
    error_message = "You are dumb...\n"
    activate_message = "You have been struck magically dumb\n"

    def magic(self, caster):
        if NewUaf.my_lev < 10:
            bprintf(self.activate_message)
            self.activate()
        else:
            bprintf("\001p{}\001 tried to dumb you\n".format(caster))


class Cripple(Disease):
    error_message = "You are crippled\n"
    activate_message = "You have been magically crippled\n"

    def magic(self, caster):
        if NewUaf.my_lev < 10:
            bprintf(self.activate_message)
            self.activate()
        else:
            bprintf("\001p{}\001 tried to cripple you\n".format(caster))


class Blind(Disease):
    error_message = "You are blind, you cannot see\n"
    activate_message = "You have been struck magically blind\n"

    def magic(self, caster):
        if NewUaf.my_lev < 10:
            bprintf(self.activate_message)
            self.activate()
        else:
            bprintf("\001p{}\001 tried to blind you\n".format(caster))


class Deaf(Disease):
    activate_message = "You have been magically deafened\n"

    def magic(self, caster):
        if NewUaf.my_lev < 10:
            bprintf(self.activate_message)
            self.activate()
        else:
            bprintf("\001p{}\001 tried to deafen you\n".format(caster))


class Force:
    def __init__(self):
        self.__action = None
        self.is_force = False

    def __add_force(self, action):
        if self.__action:
            bprintf("The compulsion to {} is overridden\n".format(self.__action))
        self.__action = action

    def check(self):
        self.is_force = True
        if self.__action:
            gamecom(self.__action)
            self.__action = None
        self.is_force = False

    def magic(self, caster, action):
        if NewUaf.my_lev < 10:
            bprintf("\001p{}\001 has forced you to {}\n".format(caster, action))
            self.__add_force(action)
        else:
            bprintf("\001p{}\001 tried to force you to {}\n".format(caster, action))


class Diseases:
    def __init__(self):
        self.dumb = Dumb()
        self.crippled = Cripple()
        self.blind = Blind()
        self.deaf = Deaf()
        self.force = Force()

    def cure(self):
        self.dumb.cure()
        self.crippled.cure()
        self.blind.cure()
        self.deaf.cure()
