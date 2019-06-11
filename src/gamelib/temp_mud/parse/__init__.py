"""
globme holds global me data
"""
from ..errors import CommandError

from ..new1.utils import get_item
from ..newuaf import NewUaf
from ..objsys import ObjSys
from ..opensys import openworld
from ..support import Item
from ..syslog import syslog
from .commands import COMMANDS

from ..actions.action import Action


def setherecom(parser):
    parser.here_ms = set_ms(parser)


class Pronouns(Action):
    @classmethod
    def action(cls, parser, user):
        yield("Current pronouns are:\n")
        yield("Me              : {}\n".format(user.name))
        yield("Myself          : {}\n".format(user.name))
        yield("It              : {}\n".format(parser.pronous['it']))
        yield("Him             : {}\n".format(parser.pronous['him']))
        yield("Her             : {}\n".format(parser.pronous['her']))
        yield("Them            : {}\n".format(parser.pronous['them']))
        if user.is_wizard:
            yield("There           : {}\n".format(parser.pronous['there']))


"""
setherecom()
{
	extern char here_ms[];
	set_ms(here_ms);
}
"""