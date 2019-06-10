"""
globme holds global me data
"""
from ..errors import CommandError, CrapupError

from ..new1.messages import MSG_WIZARD, MSG_GLOBAL
from ..new1.utils import get_item
from ..newuaf import NewUaf
from ..objsys import ObjSys, dumpitems
from ..opensys import closeworld, openworld
from ..support import Item, Player, iscarrby
from ..syslog import syslog
from .commands import COMMANDS
from .messages import Message

from gamelib.temp_mud.actions.action import Action


class Extras:
    interrupt = None
    wpnheld = None
    ROOMS = None
    GWIZ = None
    EXE = None
    EXE2 = None


def chdir(*args):
    raise NotImplementedError()


def debug2(*args):
    raise NotImplementedError()


def disle3(*args):
    raise NotImplementedError()


def examcom(*args):
    raise NotImplementedError()


def execl(*args):
    raise NotImplementedError()


def fopen(*args):
    raise NotImplementedError()


def geteuid(*args):
    raise NotImplementedError()


def getuid(*args):
    raise NotImplementedError()


def hitplayer(*args):
    raise NotImplementedError()


def iscontin(*args):
    raise NotImplementedError()


def keysetback(*args):
    raise NotImplementedError()


def keysetup(*args):
    raise NotImplementedError()


def pbfr(*args):
    raise NotImplementedError()


def system(*args):
    raise NotImplementedError()


# ----


def tsscom(parser):
    if NewUaf.my_lev < 10000:
        raise CommandError("I don't know that verb\n")
    action = parser.getreinput()
    closeworld()

    keysetback()
    if getuid() == geteuid():
        system(action)
    else:
        raise CommandError("Not permitted on this ID\n")
    keysetup()


def rmeditcom(parser):
    if user.player.tstflg(3):
        raise CommandError("Dum de dum.....\n")
    Message(
        user,
        user,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} fades out of reality\n\001".format(name=user.name),
    ).send()  # Info
    user.fade()  # CODE NUMBER
    pbfr()
    closeworld()
    try:
        chdir(Extras.ROOMS)
    except FileNotFoundError:
        yield "Warning: Can't CHDIR\n"
    system("/cs_d/aberstudent/yr2/hy8/.sunbin/emacs")
    user.message_id = None
    openworld()
    if Player.fpbns(user) is None:
        raise LooseError("You have been kicked off")
    Message(
        user,
        user,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} re-enters the normal universe\n\001".format(name=user.name),
    ).send()
    parser.read_messages()


def u_system(parser):
    if NewUaf.my_lev < 10:
        raise CommandError("You'll have to leave the game first!\n")
    user.fade()
    Message(
        user,
        user,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} has dropped into BB\n\001".format(name=user.name),
    ).send()
    closeworld()
    system("/cs_d/aberstudent/yr2/hy8/bt")
    openworld()
    user.message_id = None
    if Player.fpbns(user.name) is None:
        raise LooseError("You have been kicked off")
    parser.read_messages()
    openworld()
    Message(
        user,
        user,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} has returned to AberMud\n\001".format(name=user.name),
    ).send()


def inumcom(parser):
    if NewUaf.my_lev < 10000:
        raise CommandError("Huh ?\n")
    word = parser.brkword()
    if word is None:
        raise CommandError("What...\n")
    yield "Item Number is {}\n".format(Item.fobn(word))


def updcom(parser):
    if NewUaf.my_lev < 10:
        raise CommandError("Hmmm... you can't do that one\n")
    user.loose()
    Message(
        user,
        user,
        MSG_WIZARD,
        0,
        "[ {} has updated ]\n".format(user.name),
    ).send()
    closeworld()
    execl(Extras.EXE, "   --{----- ABERMUD -----}--   ", user.name)  # GOTOSS eek!
    yield "Eeek! someones pinched the executable!\n"


def becom(parser):
    if NewUaf.my_lev < 10:
        raise CommandError("Become what ?\n")
    x2 = parser.getreinput()
    if not x2:
        raise CommandError("To become what ?, inebriated ?\n")
    Message(
        None,
        None,
        MSG_WIZARD,
        0,
        "{} has quit, via BECOME\n".format(user.name),
    ).send()
    keysetback()
    user.loose()
    closeworld()
    execl(Extras.EXE2, "   --}----- ABERMUD ------   ", "-n{}".format(user.name))  # GOTOSS eek!
    yield "Eek! someone's just run off with mud!!!!\n"


def systat(parser):
    if NewUaf.my_lev < 10000000:
        raise CommandError("What do you think this is a DEC 10 ?\n")


def convcom(parser):
    parser.converstion_mode = parser.CONVERSATION_SAY
    yield "Type '**' on a line of its own to exit converse mode\n"


def shellcom(parser):
    if NewUaf.my_lev < 10000:
        raise CommandError("There is nothing here you can shell\n")
    parser.conversation_mode = parser,CONVERSATION_TSS
    yield "Type ** on its own on a new line to exit shell\n"


def rawcom(parser):
    if NewUaf.my_lev < 10000:
        raise CommandError("I don't know that verb\n")
    x = parser.getreinput()
    if NewUaf.my_lev == 10033 and x[0] == "!":
        user.broadcast(x[1:])
    else:
        user.broadcast("** SYSTEM : {}\n\007\007".format(x))


def rollcom(parser):
    item = get_item(parser)
    if item.item_id in [122, 123]:
        parser.gamecom("push pillar")
    else:
        raise CommandError("You can't roll that\n")


def debugcom(parser):
    if NewUaf.my_lev < 10000:
        raise CommandError("I don't know that verb\n")
    debug2()


def bugcom(parser):
    syslog("Bug by {} : {}".format(user.name, parser.getreinput()))


def typocom(parser):
    syslog("Typo by {} in {} : {}".format(user.name, user.location_id, parser.getreinput()))


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
 tsscom()
    {
    char s[128];
    extern long my_lev;
    if(my_lev<10000)
       {
       bprintf("I don't know that verb\n");
       return;
       }
    getreinput(s);
    closeworld();
    keysetback();
    if(getuid()==geteuid()) system(s);
    else bprintf("Not permitted on this ID\n");
    keysetup();
    }
 
 rmeditcom()
    {
    extern long my_lev;
    char ms[128];
    extern char globme[];
    if(!user.test_flag(3))
       {
       bprintf("Dum de dum.....\n");
       return;
       }
      
    sprintf(ms,"\001s%s\001%s fades out of reality\n\001",globme,globme);
    user.send_message(Message(globme,globme,-10113,0,ms); /* Info */
    user.fade();/* CODE NUMBER */
    pbfr();
    closeworld();
    if(chdir(ROOMS)==-1) bprintf("Warning: Can't CHDIR\n");
    sprintf(ms,"/cs_d/aberstudent/yr2/hy8/.sunbin/emacs");
    system(ms);
    user.reset_position()
    openworld();
    if(fpbns(globme)== -1)
       {
       raise LooseError("You have been kicked off");
       }
    sprintf(ms,"\001s%s\001%s re-enters the normal universe\n\001",globme,globme);
    user.send_message(Message(globme,globme,-10113,0,ms);
    parser.read_messages()
    }
 
 u_system()
    {
    extern long my_lev;
    extern char globme[];
    char x[128];
    if(my_lev<10)
       {
       bprintf("You'll have to leave the game first!\n");
       return;
       }
    user.fade()
    sprintf(x,"%s%s%s%s%s","\001s",globme,"\001",globme," has dropped into BB\n\001");
    user.send_message(Message(globme,globme,-10113,0,x);
    closeworld();
    system("/cs_d/aberstudent/yr2/iy7/bt");
    openworld();
    user.reset_position()
    if(fpbns(globme)== -1)
       {
       raise LooseError("You have been kicked off");
       }
    parser.read_messages()
    openworld();
    sprintf(x,"%s%s%s%s%s","\001s",globme,"\001",globme," has returned to AberMud\n\001");
    user.send_message(Message(globme,globme,-10113,0,x);
    }
 
 inumcom()
    {
    extern long my_lev;
    extern char wordbuf[];
    if(my_lev<10000)
       {
       bprintf("Huh ?\n");
       return;
       }
    if(brkword()== -1)
       {
       bprintf("What...\n");
       return;
       }
    bprintf("Item Number is %d\n",fobn(wordbuf));
    }
 
 updcom()
    {
    extern long my_lev;
    char x[128];
    extern char globme[];
    if(my_lev<10)
       {
       bprintf("Hmmm... you can't do that one\n");
       return;
       }
    user.loose()
    sprintf(x,"[ %s has updated ]\n",globme);
    user.send_message(Message(globme,globme,-10113,0,x);
    closeworld();
    sprintf(x,"%s",globme);
    execl(EXE,
    "   --{----- ABERMUD -----}--   ",x,0);  /* GOTOSS eek! */
    bprintf("Eeek! someones pinched the executable!\n");
    }
 
 becom()
    {
    extern char globme[];
    extern long my_lev;
    char x[128];
    char x2[128];
    if(my_lev<10)
       {
       bprintf("Become what ?\n");
       return;
       }
    getreinput(x2);
    if(!strlen(x2))
       {
       bprintf("To become what ?, inebriated ?\n");
       return;
       }
    sprintf(x,"%s has quit, via BECOME\n",globme);
    user.send_message(Message("","",-10113,0,x);
    keysetback();
    user.loose();
    closeworld();
    sprintf(x,"-n%s",x2);
    execl(EXE2,"   --}----- ABERMUD ------   ",x,0);	/* GOTOSS eek! */
    bprintf("Eek! someone's just run off with mud!!!!\n");
    }
 
 systat()
    {
    extern long my_lev;
    if(my_lev<10000000)
       {
       bprintf("What do you think this is a DEC 10 ?\n");
       return;
       }
    }
 
 convcom()
    {
    parser.converstion_mode = parser.CONVERSATION_SAY
    bprintf("Type '**' on a line of its own to exit converse mode\n");
    }
 
 shellcom()
    {
    extern long my_lev;
    if(my_lev<10000)
       {
       bprintf("There is nothing here you can shell\n");
       return;
       }
    parser.converstion_mode = parser.CONVERSATION_TSS
    bprintf("Type ** on its own on a new line to exit shell\n");
    }
 
 rawcom()
    {
    extern long my_lev;
    char x[100],y[100];
    if(my_lev<10000)
       {
       bprintf("I don't know that verb\n");
       return;
       }
    getreinput(x);
    if((my_lev==10033)&&(x[0]=='!'))
       {
       user.broadcast(x+1)
       return;
       }
    else
       {
       sprintf(y,"%s%s%s","** SYSTEM : ",x,"\n\007\007");
       user.broadcast(y);
       }
    }
 
 rollcom()
    {
    auto long  a,b;
    b=ohereandget(&a);
    if(b== -1) return;
    switch(a)
       {
       case 122:;
       case 123:
          gamecom("push pillar");
          break;
       default:
          bprintf("You can't roll that\n");
       }
    }
 
long brmode=0;
 
 debugcom()
    {
    extern long my_lev;
    if(my_lev<10000)
       {
       bprintf("I don't know that verb\n");
       return;
       }
    debug2();
    }

bugcom()
{
	char x[120];
	extern char globme[];
	getreinput(x);
	syslog("Bug by %s : %s",globme,x);
}

typocom()
{
	char x[120],y[32];
	extern char globme[];
	sprintf(y,"%s in %d",globme,user.location_id);
	getreinput(x);
	syslog("Typo by %s : %s",y,x);
}

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