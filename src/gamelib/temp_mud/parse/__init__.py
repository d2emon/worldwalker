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


def look_cmd(parser):
    word = parser.brkword()
    if word is None:
        user.look(True)
        return
    if word == "at":
        return examcom()
    if word != "in" and word != "into":
        return

    word = parser.brkword()
    if word is None:
        raise CommandError("In what ?\n")

    item = Item.fobna(word)
    if item is None:
        raise CommandError("What ?\n")
    if not item.tstbit(14):
        raise CommandError("That isn't a container\n")
    if item.tstbit(2) and item.state != 0:
        raise CommandError("It's closed!\n")

    yield "The {} contains:\n".format(item.name)
    item.aobjsat(3)


def set_ms(parser):
    if NewUaf.my_lev < 10 and user.name != "Lorry":
        raise CommandError("No way !\n")
    else:
        return parser.getreinput()


def setmincom(parser):
    parser.min_ms = set_ms(parser)


def setincom(parser):
    parser.in_ms = set_ms(parser)


def setoutcom(parser):
    parser.out_ms = set_ms(parser)


def setmoutcom(parser):
    parser.mout_ms = set_ms(parser)


def setherecom(parser):
    parser.here_ms = set_ms(parser)


def digcom(parser):
    item = Item(186)
    if item.loc == user.location_id and item.is_destroyed:
        yield "You uncover a stone slab!\n"
        item.create()
        return

    if user.location_id != -172 and user.location_id != -192:
        raise CommandError("You find nothing.\n")

    item = Item(176)
    if item.state == 0:
        raise CommandError("You widen the hole, but with little effect.\n")
    item.state = 0
    yield "You rapidly dig through to another passage.\n"


def emptycom(parser):
    container = get_item(parser)
    for item_id in range(ObjSys.numobs):
        item = Item(item_id)
        if not iscontin(item, container):
            item.set_location(user.location_id, 1)
            yield "You empty the {} from the {}\n".format(item.name, container.name)
            parser.gamecom("drop {}".format(item.name))
            pbfr()
            openworld()


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
look_cmd()
{
	int a;
	long brhold;
	extern long brmode;
	extern char wordbuf[];
	if(brkword()==-1)
	{
          brhold=brmode;
          brmode=0;

          user.look(parser.brief, parser.mode == parser.MODE_GAME)
          if parser.user.location.no_brief:
              parser.brief = False

          brmode=brhold;
          return;
        }
        if(strcmp(wordbuf,"at")==0)
        {
        	examcom();
        	return;
        }
        if((strcmp(wordbuf,"in"))&&(strcmp(wordbuf,"into")))
        {
        	return;
        }
        if(brkword()==-1)
        {
        	bprintf("In what ?\n");
        	return;
        }
        a=fobna(wordbuf);
	if(a==-1)
	{
		bprintf("What ?\n");
		return;
	}
	if(!Item(a).test_bit(14))
	{
		bprintf("That isn't a container\n");
		return;
	}
	if((Item(a).test_bit(2))&&(state(a)!=0))
	{
		bprintf("It's closed!\n");
		return;
	}
	bprintf("The %s contains:\n",Item(a).name);
	aobjsat(a,3);
}
	
set_ms(x)
char *x;
{
	extern long my_lev;
	extern char globme[];
	if((my_lev<10)&&(strcmp(globme,"Lorry")))
	{
		bprintf("No way !\n");
	}
	else
	{
		getreinput(x);
	}
	return;
}

setmincom()
{
	extern char min_ms[];
	set_ms(min_ms);
}
setincom()
{
	extern char min_ms[];
	set_ms(in_ms);
}
setoutcom()
{
	extern char out_ms[];
	set_ms(out_ms);
}
setmoutcom()
{
	extern char mout_ms[];
	set_ms(mout_ms);
}

setherecom()
{
	extern char here_ms[];
	set_ms(here_ms);
}

digcom()
{
	if((Item(186).location==user.location_id)&&(Item(186).is_destroyed))
	{
		bprintf("You uncover a stone slab!\n");
		Item(186).create();
		return;
	}
	if((user.location_id!=-172)&&(user.location_id!=-192))
	{
		bprintf("You find nothing.\n");
		return;
	}
	if(state(176)==0)
	{
		bprintf("You widen the hole, but with little effect.\n");
		return;
	}
	setstate(176,0);
	bprintf("You rapidly dig through to another passage.\n");
}

emptycom()
{
	long a,b;
	extern long numobs;
	char x[81];
	b=ohereandget(&a);
	if(b==-1) return;
	b=0;
	while(b<numobs)
	{
		if(iscontin(b,a))
		{
			Item(b).set_location(user,1);
			bprintf("You empty the %s from the %s\n",Item(b).name,Item(a).name);
			sprintf(x,"drop %s",Item(b).name);
			gamecom(x);
			pbfr();
			openworld();
		}
		b++;
	}
}

"""