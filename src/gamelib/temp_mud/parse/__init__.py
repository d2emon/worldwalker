"""
globme holds global me data
"""
from ..errors import CommandError

from ..blood import Blood
from ..bprintf import bprintf
from ..magic import randperc
from ..new1.disease import DISEASES
from ..new1.messages import MSG_WIZARD, MSG_GLOBAL
from ..newuaf import NewUaf
from ..objsys import dumpitems
from ..support import Item, Player, syslog, iscarrby
from ..tk import Tk, trapch, broad
from .commands import COMMANDS
from .messages import Message


"""
Objects held in format
 
[Short Text]
[4 Long texts]
[Max State]


Objects in text file in form
 
Stam:state:loc:flag
"""


class Extras:
    interrupt = None
    wpnheld = None
    i_setup = None
    ROOMS = None
    GWIZ = None


def disle3(*args):
    raise NotImplementedError()


def fopen(*args):
    raise NotImplementedError()


def hitplayer(*args):
    raise NotImplementedError()


def time(*args):
    raise NotImplementedError()


class Parse:
    __debug_mode = False

    __strbuf = ""
    wordbuf = ""
    __wd_it = ""
    __wd_him = ""
    __wd_her = ""
    __wd_them = ""
    __wd_there = ""
    __stp = 0

    __verbtxt = []
    __verbnum = []

    __exittxt = []
    __exitnum = []

    in_ms = "has arrived."
    out_ms = ""
    __mout_ms = "vanishes in a puff of smoke."
    __min_ms = "appears with an ear-splitting bang."
    __here_ms = "is here"

    __tdes = 0
    __vdes = 0
    __rdes = 0
    __ades = 0
    zapped = False

    __me_ivct = 0
    __last_io_interrupt = 0

    __me_drunk = 0

    me_cal = 0

    __br_mode = False

    @classmethod
    def pncom(cls):
        bprintf("Current pronouns are:\n")
        bprintf("Me              : {}\n".format(Tk.globme))
        bprintf("Myself          : {}\n".format(Tk.globme))
        bprintf("It              : {}\n".format(cls.__wd_it))
        bprintf("Him             : {}\n".format(cls.__wd_him))
        bprintf("Her             : {}\n".format(cls.__wd_her))
        bprintf("Them            : {}\n".format(cls.__wd_them))
        if NewUaf.my_lev > 9:
            bprintf("There           : {}\n".format(cls.__wd_there))

    @classmethod
    def gamecom(cls, action):
        try:
            if action != "!":
                cls.__strbuf = action
            if action == ".q":
                action = ""
                # Otherwise drops out after command
            cls.__stp = 0
            if not action:
                return True
            # if action == "!":
            #     action = cls.__strbuf
            word = cls.brkword()
            if word is None:
                raise CommandError("Pardon ?\n")
            verb = cls.__chkverb(word)
            if verb is None:
                raise CommandError("I don't know that verb\n")
            for line in verb.do_action(cls):
                bprintf(line)
        except CommandError as e:
            bprintf(e)
            return False

    @classmethod
    def brkword(cls):
        started = False
        for cls.__stp, character in enumerate(cls.__strbuf[cls.__stp:]):
            if character == ' ':
                if started:
                    break
                else:
                    continue
            started = True
            cls.wordbuf += character
        cls.wordbuf.lower()
        if cls.wordbuf == "it":
            cls.wordbuf = cls.__wd_it
        if cls.wordbuf == "them":
            cls.wordbuf = cls.__wd_them
        if cls.wordbuf == "him":
            cls.wordbuf = cls.__wd_him
        if cls.wordbuf == "her":
            cls.wordbuf = cls.__wd_her
        if cls.wordbuf == "me":
            cls.wordbuf = Tk.globme
        if cls.wordbuf == "myself":
            cls.wordbuf = Tk.globme
        if cls.wordbuf == "there":
            cls.wordbuf = cls.__wd_there
        if len(cls.wordbuf) <= 0:
            return None
        return cls.wordbuf

    @classmethod
    def chklist(cls, word, data):
        best_value = 0
        best_item = None
        word = word.lower()
        for item in data:
            for verb in item.verbs:
                value = cls.__match(word, verb)
                if value < 5:
                    continue
                if value < best_value:
                    continue
                best_value = value
                best_item = item
        return best_item

    @classmethod
    def __match(cls, x, y):
        if x == y:
            return 10000
        if y == "reset":
            return -1
        if not x:
            return 0

        match_count = 0
        for n in range(min(len(x), len(y))):
            if x[n] != y[n]:
                continue
            if n == 0:
                match_count += 3
            elif n == 1:
                match_count += 2
            else:
                match_count += 1
        return match_count

    @classmethod
    def __chkverb(cls, word):
        return cls.chklist(word, COMMANDS)

    @classmethod
    def eorte(cls):
        ctm = time()
        if ctm - cls.__last_io_interrupt > 2:
            Extras.interrupt = True
        if Extras.interrupt:
            cls.__last_io_interrupt = ctm
        if cls.__me_ivct:
            cls.__me_ivct -= 1
        if cls.__me_ivct == 1:
            Player(Tk.mynum).visible = 0
        if cls.me_cal:
            cls.me_cal = False
            cls.calibme()
        if cls.__tdes:
            cls.__dosumm(cls.__ades)
        if Blood.in_fight:
            fight_with = Player(Blood.fighting)
            if fight_with.location != Tk.curch:
                Blood.fighting = -1
                Blood.in_fight = 0
            if not fight_with.exists:
                Blood.fighting = -1
                Blood.in_fight = 0
            if Blood.in_fight and Extras.interrupt:
                Blood.in_fight = 0
                hitplayer(fight_with, Extras.wpnheld)
        if Item(18).is_worn_by(Tk.mynum) or randperc() < 10:
            NewUaf.my_str += 1
            if Extras.i_setup:
                cls.calibme()
        DISEASES.force.check()
        if cls.__me_drunk > 0:
            cls.__me_drunk -= 1
            if not DISEASES.dumb.active:
                cls.gamecom("hiccup")
        Extras.interrupt = False

    @classmethod
    def openroom(cls, room_id, mode):
        return fopen(Extras.ROOMS + (-room_id), mode)

    @classmethod
    def calibme(cls):
        """
        Routine to correct me in user file

        :return:
        """
        if not Extras.i_setup:
            return

        new_level = cls.__level_of(NewUaf.my_sco)
        player = Player(Tk.mynum)

        if new_level != NewUaf.my_lev:
            NewUaf.my_lev = new_level
            bprintf("You are now {} ".format(Tk.globme))
            syslog("{} to level {}".format(Tk.globme, NewUaf.my_lev))
            disle3(new_level, NewUaf.my_sex)
            Message(
                Tk,
                Tk,
                MSG_WIZARD,
                player.location,
                "\001p{}\001 is now level {}\n".format(Tk.globme, NewUaf.my_lev),
            ).send()
            if new_level == 10:
                bprintf("\001f{}\001".format(Extras.GWIZ))

        player.level = NewUaf.my_lev
        if NewUaf.my_str > 30 + 10 * NewUaf.my_lev:
            NewUaf.my_str = 30 + 10 * NewUaf.my_lev
        player.strength = NewUaf.my_str
        player.sex = NewUaf.my_sex
        player.weapon = Extras.wpnheld

    @classmethod
    def __level_of(cls, score):
        score = score / 2  # Scaling factor
        if NewUaf.my_lev > 10:
            return NewUaf.my_lev
        if score < 500:
            return 1
        if score < 1000:
            return 2
        if score < 3000:
            return 3
        if score < 6000:
            return 4
        if score < 10000:
            return 5
        if score < 20000:
            return 6
        if score < 32000:
            return 7
        if score < 44000:
            return 8
        if score < 70000:
            return 9
        return 10

    @classmethod
    def getreinput(cls):
        text = ""
        while cls.__strbuf[cls.__stp] == ' ':
            cls.__stp += 1
        while cls.__stp < len(cls.__strbuf):
            text += cls.__strbuf[cls.__stp]
            cls.__stp += 1
        return text

    @classmethod
    def dogive(cls, item, player):
        if NewUaf.my_lev < 10 and player.location != Tk.curch:
            raise CommandError("They are not here\n")
        if not iscarrby(item, Tk.mynum):
            raise CommandError("They are not here\n")
        if not player.can_carry:
            raise CommandError("They can't carry that\n")
        if NewUaf.my_lev < 10 and item.item_id == 32:
            raise CommandError("It doesn't wish to be given away.....\n")
        item.setoloc(player.player_id, 1)
        Message(
            player,
            Tk,
            -10011,
            Tk.curch,
            "\001p{}\001 gives you the {}\n".format(Tk.globme, item.name),
        ).send()

    @classmethod
    def __dosumm(cls, location):
        Message(
            Tk,
            Tk,
            -10000,
            Tk.curch,
            "\001s{name}\001{name} vanishes in a puff of smoke\n\001".format(name=Tk.globme),
        ).send()
        text = "\001s{name}\001{name} appears in a puff of smoke\n\001".format(name=Tk.globme)
        dumpitems()
        Tk.curch = location
        Message(
            Tk,
            Tk,
            MSG_GLOBAL,
            Tk.curch,
            text,
        ).send()
        trapch(Tk.curch)


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
    if Player(Tk.mynum).tstflg(3):
        raise CommandError("Dum de dum.....\n")
    Message(
        Tk,
        Tk,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} fades out of reality\n\001".format(name=Tk.globme),
    ).send()  # Info
    Tk.cms = -2  # CODE NUMBER
    update(Tk.globme)
    pbfr()
    closeworld()
    try:
        chdir(Extras.ROOMS)
    except FileNotFoundError:
        yield "Warning: Can't CHDIR\n"
    system("/cs_d/aberstudent/yr2/hy8/.sunbin/emacs")
    Tk.cms = None
    openworld()
    if Player.fpbns(Tk.globme) is None:
        loseme()
        raise CrapupError("You have been kicked off")
    Message(
        Tk,
        Tk,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} re-enters the normal universe\n\001".format(name=Tk.globme),
    ).send()
    rte()


def u_system(parser):
    if NewUaf.my_lev < 10:
        raise CommandError("You'll have to leave the game first!\n")
    Tk.cms = -2
    update(Tk.globme)
    Message(
        Tk,
        Tk,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} has dropped into BB\n\001".format(name=Tk.globme),
    ).send()
    closeworld()
    system("/cs_d/aberstudent/yr2/hy8/bt")
    openworld()
    Tk.cms = None
    if Player.fpbns(Tk.globme) is None:
        loseme()
        raise CrapupError("You have been kicked off")
    rte()
    openworld()
    Message(
        Tk,
        Tk,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} has returned to AberMud\n\001".format(name=Tk.globme),
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
    loseme()
    Message(
        Tk,
        Tk,
        MSG_WIZARD,
        0,
        "[ {} has updated ]\n".format(Tk.globme),
    ).send()
    closeworld()
    execl(Extras.EXE, "   --{----- ABERMUD -----}--   ", Tk.globme)  # GOTOSS eek!
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
        "{} has quit, via BECOME\n".format(Tk.globme),
    ).send()
    keysetback()
    loseme()
    closeworld()
    execl(Extras.EXE2, "   --}----- ABERMUD ------   ", "-n{}".format(Tk.globme))  # GOTOSS eek!
    yield "Eek! someone's just run off with mud!!!!\n"


def systat(parser):
    if NewUaf.my_lev < 10000000:
        raise CommandError("What do you think this is a DEC 10 ?\n")


def convcom(parser):
    Extras.convflg = 1
    yield "Type '**' on a line of its own to exit converse mode\n"


def shellcom(parser):
    if NewUaf.my_lev < 10000:
        raise CommandError("There is nothing here you can shell\n")
    Extras.convflg = 2
    yield "Type ** on its own on a new line to exit shell\n"


def rawcom(parser):
    if NewUaf.my_lev < 10000:
        raise CommandError("I don't know that verb\n")
    x = parser.getreinput()
    if NewUaf.my_lev == 10033 and x[0] == "!":
        broad(x[1:])
    else:
        broad("** SYSTEM : {}\n\007\007".format(x))


def rollcom(parser):
    item = get_item()
    if item.item_id in [122, 123]:
        parser.gamecom("push pillar")
    else:
        raise CommandError("You can't roll that\n")


def debugcom(parser):
    if NewUaf.my_lev < 10000:
        raise CommandError("I don't know that verb\n")
    debug2()


def bugcom(parser):
    syslog("Bug by {} : {}".format(Tk.globme, parser.getreinput()))


def typocom(parser):
    syslog("Typo by {} in {} : {}".format(Tk.globme, Tk.curch, parser.getreinput()))


"""
look_cmd()
{
	int a;
	long brhold;
	extern long brmode;
	extern char wordbuf[];
        extern long curch;
    wordbuf = cls.brkword()
    if wordbuf is None:
	{
          brhold=brmode;
          brmode=0;
          lookin(curch);
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
    wordbuf = cls.brkword()
    if wordbuf is None:
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
	if(!otstbit(a,14))
	{
		bprintf("That isn't a container\n");
		return;
	}
	if((otstbit(a,2))&&(state(a)!=0))
	{
		bprintf("It's closed!\n");
		return;
	}
	bprintf("The %s contains:\n",oname(a));
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
        x = cls.getreinput();
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
        extern long curch;
	if((oloc(186)==curch)&&(isdest(186)))
	{
		bprintf("You uncover a stone slab!\n");
		ocreate(186);
		return;
	}
	if((curch!=-172)&&(curch!=-192))
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
"""
"""

emptycom()
{
	long a,b;
	extern long numobs;
        extern long mynum;
	char x[81];
    a = get_item()
	b=0;
	while(b<numobs)
	{
		if(iscontin(b,a))
		{
			setoloc(b,mynum,1);
			bprintf("You empty the %s from the %s\n",oname(b),oname(a));
			sprintf(x,"drop %s",oname(b));
			cls.gamecom(x);
			pbfr();
			openworld();
		}
		b++;
	}
}
"""
