"""
globme holds global me data
"""
from ..errors import CommandError, CrapupError

from ..blood import Blood
from ..bprintf import bprintf
from ..magic import randperc
from ..new1.disease import DISEASES
from ..new1.messages import MSG_WIZARD, MSG_GLOBAL
from ..new1.utils import get_item
from ..newuaf import NewUaf
from ..objsys import ObjSys, dumpitems
from ..opensys import closeworld, openworld
from ..support import Item, Player, iscarrby
from ..syslog import syslog
from ..tk import trapch, loseme
from .commands import COMMANDS
from .messages import Message

from gamelib.temp_mud.actions.action import Action


class Extras:
    interrupt = None
    wpnheld = None
    i_setup = None
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


def lookin(*args):
    raise NotImplementedError()


def pbfr(*args):
    raise NotImplementedError()


def rte(*args):
    raise NotImplementedError()


def system(*args):
    raise NotImplementedError()


def time(*args):
    raise NotImplementedError()


def update(*args):
    raise NotImplementedError()


class Parse:
    __verbtxt = []
    __verbnum = []

    __exittxt = []
    __exitnum = []

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
            user.player.visible = 0
        if cls.me_cal:
            cls.me_cal = False
            cls.calibme()
        if cls.__tdes:
            cls.__dosumm(cls.__ades)
        if Blood.in_fight:
            fight_with = Player(Blood.fighting)
            if fight_with.location != user.location_id:
                Blood.fighting = -1
                Blood.in_fight = 0
            if not fight_with.exists:
                Blood.fighting = -1
                Blood.in_fight = 0
            if Blood.in_fight and Extras.interrupt:
                Blood.in_fight = 0
                hitplayer(fight_with, Extras.wpnheld)
        if Item(18).is_worn_by(user.player) or randperc() < 10:
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
        player = user.player

        if new_level != NewUaf.my_lev:
            NewUaf.my_lev = new_level
            bprintf("You are now {} ".format(user.name))
            syslog("{} to level {}".format(user.name, NewUaf.my_lev))
            disle3(new_level, NewUaf.my_sex)
            Message(
                user,
                user,
                MSG_WIZARD,
                player.location,
                "\001p{}\001 is now level {}\n".format(user.name, NewUaf.my_lev),
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
        if NewUaf.my_lev < 10 and player.location != user.location_id:
            raise CommandError("They are not here\n")
        if not iscarrby(item, user.player):
            raise CommandError("They are not here\n")
        if not player.can_carry:
            raise CommandError("They can't carry that\n")
        if NewUaf.my_lev < 10 and item.item_id == 32:
            raise CommandError("It doesn't wish to be given away.....\n")
        item.set_location(player.player_id, 1)
        Message(
            player,
            user,
            -10011,
            user.location_id,
            "\001p{}\001 gives you the {}\n".format(user.name, item.name),
        ).send()

    @classmethod
    def __dosumm(cls, location):
        Message(
            user,
            user,
            -10000,
            user.location_id,
            "\001s{name}\001{name} vanishes in a puff of smoke\n\001".format(name=user.name),
        ).send()
        text = "\001s{name}\001{name} appears in a puff of smoke\n\001".format(name=user.name)
        dumpitems()
        user.location_id = location
        Message(
            user,
            user,
            MSG_GLOBAL,
            user.location_id,
            text,
        ).send()
        trapch(user.location_id)


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
    user.message_id = -2  # CODE NUMBER
    update(user.name)
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
        loseme()
        raise CrapupError("You have been kicked off")
    Message(
        user,
        user,
        MSG_WIZARD,
        0,
        "\001s{name}\001{name} re-enters the normal universe\n\001".format(name=user.name),
    ).send()
    rte()


def u_system(parser):
    if NewUaf.my_lev < 10:
        raise CommandError("You'll have to leave the game first!\n")
    user.message_id = -2
    update(user.name)
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
        loseme()
        raise CrapupError("You have been kicked off")
    rte()
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
    loseme()
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
    loseme()
    closeworld()
    execl(Extras.EXE2, "   --}----- ABERMUD ------   ", "-n{}".format(user.name))  # GOTOSS eek!
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
        Broadcast(x[1:]).send(user)
    else:
        Broadcast("** SYSTEM : {}\n\007\007".format(x)).send(user)


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
        brhold = parser.brmode
        parser.brmode = 0
        lookin(user.location_id)
        parser.brmode = brhold
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
 dodirn(n)
    {
    extern long curch;
    extern long mynum;
    extern char globme[];
    extern long ex_dat[];
    extern long ail_blind;
    extern char in_ms[],out_ms[];
    char block[256],x[32];
    long  newch,fl,i;
    extern long in_fight;
    }
 
long tdes=0;
long vdes=0;
long rdes=0;
long ades=0;
long zapped;

 gamrcv(blok)
 long *blok;
    {
    extern long zapped;
    extern long vdes,tdes,rdes,ades;
    extern char globme[];
    auto long  zb[32];
    long *i;
    extern long curch;
    extern long my_lev;
    extern long my_sco;
    extern long my_str;
    extern long snoopd;
    extern long fl_com;
    char ms[128];
    char nam1[40],nam2[40],text[256],nameme[40];
    long isme;
    extern long fighting,in_fight;
    strcpy(nameme,globme);
    lowercase(nameme);
    isme=split(blok,nam1,nam2,text,nameme);
    i=(long *)text;
    if((blok[1]== -20000)&&(fpbns(nam1)==fighting))
       {
       in_fight=0;
       fighting= -1;
       }
    if(blok[1]<-10099)
       {
       new1rcv(isme,blok[0],nam1,nam2,blok[1],text);
       return;
       }
    switch(blok[1])
       {
       case -9900:
          Player(i[0]).visible = i[1];break;
       case -666:
          bprintf("Something Very Evil Has Just Happened...\n");
          loseme();
          crapup("Bye Bye Cruel World....");
       case -599:
          if(isme)
             {
             sscanf(text,"%d.%d.%d.",&my_lev,&my_sco,&my_str);
             calibme();
             }
          break;
       case -750:
          if(isme)
             {
             if(fpbns(nam2)!= -1) loseme();
             closeworld();
             printf("***HALT\n");
             exit(0);
             }
       case -400:
          if(isme) snoopd= -1;
          break;
       case -401:
          if(isme)
             {
             snoopd=fpbns(nam2);
             }
          break;
       case -10000:
          if((isme!=1)&&(blok[0]==curch))
             {
             bprintf("%s",text);
             }
          break;
       case -10030:
          wthrrcv(blok[0]);break;
       case -10021:
          if(curch==blok[0])
             {
             if(isme==1)
                {
                rdes=1;
                vdes=i[0];
                bloodrcv((long *)text,isme);
                }
             }
          break;
       case -10020:
          if(isme==1)
             {
             ades=blok[0];
             if(my_lev<10)
                {
                bprintf("You drop everything you have as you are summoned by \001p%s\001\n",nam2);
                }
             else
                {
                bprintf("\001p%s\001 tried to summon you\n",nam2);
                return;
                }
             tdes=1;
             }
          break;
       case -10001:
          if(isme==1)
             {
             if (my_lev>10)
                bprintf("\001p%s\001 cast a lightning bolt at you\n", nam2);
             else
                /* You are in the .... */
                {
                bprintf("A massive lightning bolt arcs down out of the sky to strike");
                sprintf(zb,"[ \001p%s\001 has just been zapped by \001p%s\001 and terminated ]\n",
                    globme, nam2);
                user.send_message(Message(globme,globme,-10113,curch,zb);
                bprintf(" you between\nthe eyes\n");
                zapped=1;
                delpers(globme);
                sprintf(zb,"\001s%s\001%s has just died.\n\001",globme,globme);
                user.send_message(Message(globme,globme,-10000,curch,zb);
                loseme();
                bprintf("You have been utterly destroyed by %s\n",nam2);

                crapup("Bye Bye.... Slain By Lightning");
                }
             }
          else if (blok[0]==curch)
             bprintf("\001cA massive lightning bolt strikes \001\001D%s\001\001c\n\001", nam1);
          break;
       case -10002:
          if(isme!=1)
             {
             if (blok[0]==curch||my_lev>9)
                 bprintf("\001P%s\001\001d shouts '%s'\n\001", nam2, text);
             else
                bprintf("\001dA voice shouts '%s'\n\001",text);
             }
          break;
       case -10003:
          if(isme!=1)
             {
             if (blok[0]==curch)
                bprintf("\001P%s\001\001d says '%s'\n\001", nam2, text);
             }
          break;
       case -10004:
          if(isme)
             bprintf("\001P%s\001\001d tells you '%s'\n\001",nam2,text);
          break;
       case -10010:
          if(isme==1)
             {
             loseme();
             crapup("You have been kicked off");
             }
          else
             bprintf("%s has been kicked off\n",nam1);
          break;
       case -10011:
          if(isme==1)
             {
             bprintf("%s",text);
             }
          break;
          }
    }
 
long me_ivct=0;
long last_io_interrupt=0;

eorte()
{
    extern long mynum,me_ivct;
    extern long me_drunk;
    extern long ail_dumb;
    extern long curch,tdes,rdes,vdes,ades;
    extern long me_cal;
    extern long wpnheld;
    extern long my_str;
    extern long i_setup;
    extern long interrupt;
    extern long fighting,in_fight;
    long ctm;
    time(&ctm);
    if(ctm-last_io_interrupt>2) interrupt=1;
    if(interrupt) last_io_interrupt=ctm;
    if(me_ivct) me_ivct--;
    if(me_ivct==1) Player(mynum).visible = 0
    if(me_cal)
       {
       me_cal=0;
       calibme();
       }
    if(tdes) dosumm(ades);
    if(in_fight)
    {
       if(Player(fighting).location!=curch)
          {
          fighting= -1;
          in_fight=0;
          }
       if(not Player(fighting).exists)
          {
          fighting= -1;
          in_fight=0;
          }
       if(in_fight)
          {
          if(interrupt)
             {
             in_fight=0;
             hitplayer(fighting,wpnheld);
             }
          }
       }
    if((iswornby(18,mynum))||(randperc()<10))
       {
       my_str++;
       if(i_setup) calibme();
       }
    forchk();
    if(me_drunk>0)
       {
       me_drunk--;
       if(!ail_dumb) gamecom("hiccup");
       }
       interrupt=0;
    }
 
long me_drunk=0;
 
FILE *openroom(n,mod)
    {
    long  blob[64];
    FILE *x;
    sprintf(blob,"%s%d",ROOMS,-n);
    x=fopen(blob,mod);
    return(x);
    }
    
long me_cal=0;

 rescom()
    {
    extern long my_lev;
    extern long objinfo[],numobs;
    FILE *b;
    char dabk[32];
    long i;
    FILE *a;
    if(my_lev<10)
       {
       bprintf("What ?\n");
       return;
       }
    Broadcast("Reset in progress....\nReset Completed....\n").send(user);
    b=openlock(RESET_DATA,"r");
    sec_read(b,objinfo,0,4*numobs);
    fcloselock(b);
    time(&i);
    a=fopen(RESET_T,"w");
    fprintf(a,"Last Reset At %s\n",ctime(&i));
    fclose(a);
    a=fopen(RESET_N,"w");
    fprintf(a,"%ld\n",i);
    fclose(a);
    resetplayers();
    }
 
 lightning()
    {
    extern long my_lev;
    long  vic;
    extern char wordbuf[];
    extern char globme[];
    extern long curch;
    if(my_lev<10)
       {
       bprintf("Your spell fails.....\n");
       return;
       }
    if(brkword()== -1)
       {
       bprintf("But who do you wish to blast into pieces....\n");
       return;
       }
    vic=fpbn(wordbuf);
    if(vic== -1)
       {
       bprintf("There is no one on with that name\n");
       return;
       }
    user.send_message(Message(Player(vic).name,globme,-10001,Player(vic).location,"");
    syslog("%s zapped %s",globme,Player(vic).name);
    if(vic>15)woundmn(vic,10000); /* DIE */
    Broadcast("\001dYou hear an ominous clap of thunder in the distance\n\001").send(user);
    }

 eatcom()
    {
    long b;
    extern char wordbuf[];
    extern long curch;
    extern long mynum;
    extern long curch;
    extern long my_str;
    extern long my_lev;
    extern long my_sco;
    if(brkword()== -1)
       {
       bprintf("What\n");
       return;
       }

    if((curch== -609)&&(!strcmp(wordbuf,"water"))) strcpy(wordbuf,"spring");
    if(!strcmp(wordbuf,"from")) brkword();
    b=fobna(wordbuf);
    if(b== -1)
       {
       bprintf("There isn't one of those here\n");
       return;
       }

    switch(b)
       {
       case 11:
          bprintf("You feel funny, and then pass out\n");
          bprintf("You wake up elsewhere....\n");
          teletrap(-1076);
          break;
       case 75:
          bprintf("very refreshing\n");
          break;
       case 175:
          if(my_lev<3)
             {
             my_sco+=40;
             calibme();
             bprintf("You feel a wave of energy sweeping through you.\n");
             break;
             }
          else
             {
             bprintf("Faintly magical by the taste.\n");
             if(my_str<40) my_str+=2;
             calibme();
             }
          break;
       default:
          if(Item(b).test_bit(6))
             {
             destroy(b);
             bprintf("Ok....\n");
             my_str+=12;
             calibme();
             }
          else
             bprintf("Thats sure not the latest in health food....\n");
          break;
       }
    }
 
 calibme()
    {
    /* Routine to correct me in user file */
    long  a;
    extern long mynum,my_sco,my_lev,my_str,my_sex,wpnheld;
    extern char globme[];
    long  b;
    char *sp[128];
    extern long i_setup;
    if(!i_setup) return;
    b=levelof(my_sco);
    if(b!=my_lev)
       {
       my_lev=b;
       bprintf("You are now %s ",globme);
       syslog("%s to level %d",globme,b);
       disle3(b,my_sex);
       sprintf(sp,"\001p%s\001 is now level %d\n",globme,my_lev);
       user.send_message(Message(globme,globme,-10113,Player(mynum).location,sp);
       if(b==10) bprintf("\001f%s\001",GWIZ);
       }
    Player(mynum).level = my_lev
    if(my_str>(30+10*my_lev)) my_str=30+10*my_lev;
    Player(mynum).strength = my_str
    Player(mynum).sex = my_sex
    Player(mynum).weapon = wpnheld
    }
 
 levelof(score)
    {
    extern long my_lev;
    score=score/2;  /* Scaling factor */
    if(my_lev>10) return(my_lev);
    if(score<500) return(1);
    if(score<1000) return(2);
    if(score<3000) return(3);
    if(score<6000) return(4);
    if(score<10000) return(5);
    if(score<20000) return(6);
    if(score<32000) return(7);
    if(score<44000) return(8);
    if(score<70000) return(9);
    return(10);
    }
 
 playcom()
    {
    extern char wordbuf[];
    extern long curch;
    extern long mynum;
    long  a,b;
    if(brkword()== -1)
       {
       bprintf("Play what ?\n");
       return;
       }
    a=fobna(wordbuf);
    if(a== -1)
       {
       bprintf("That isn't here\n");
       return;
       }
    if(!user.is_available(a))
       {
       bprintf("That isn't here\n");
       return;
       }
    }

 getreinput(blob)
    {
    extern long stp;
    extern char strbuf[];
    strcpy(blob,"");
    while(strbuf[stp]==' ') stp++;
    while(strbuf[stp]) addchar(blob,strbuf[stp++]);
    }

 shoutcom()
    {
    extern long curch,my_lev;
    extern char globme[];
    auto char blob[200];
    if(chkdumb()) return;
    getreinput(blob);
    if(my_lev>9)
       user.send_message(Message(globme,globme,-10104,curch,blob);
    else
       user.send_message(Message(globme,globme,-10002,curch,blob);
    bprintf("Ok\n");
    }
 
 saycom()
    {
    extern long curch;
    extern char globme[];
    auto char blob[200];
    if(chkdumb()) return;
    getreinput(blob);
    user.send_message(Message(globme,globme,-10003,curch,blob);
    bprintf("You say '%s'\n",blob);
    }

 tellcom()
    {
    extern long curch;
    extern char wordbuf[],globme[];
    char blob[200];
    long  a,b;
    if(chkdumb()) return;
    if(brkword()== -1)
       {
       bprintf("Tell who ?\n");
       return;
       }
    b=fpbn(wordbuf);
    if(b== -1)
       {
       bprintf("No one with that name is playing\n");
       return;
       }
    getreinput(blob);
    user.send_message(Message(Player(b).name,globme,-10004,curch,blob);
    }
 
 scorecom()
    {
    extern long my_str,my_lev,my_sco;
    extern long my_sex;
    extern char globme[];
    if(my_lev==1)
       {
       bprintf("Your strength is %d\n",my_str);
       return;
       }
    else
       bprintf("Your strength is %d(from %d),Your score is %d\nThis ranks you as %s ",
          my_str,50+8*my_lev,my_sco,globme);
    disle3(my_lev,my_sex);
    }

 exorcom()
    {
    long  x,a;
    extern long curch;
    extern long my_lev;
    extern char globme[];
    extern char wordbuf[];
    if(my_lev<10)
       {
       bprintf("No chance....\n");
       return;
       }
    if(brkword()== -1)
       {
       bprintf("Exorcise who ?\n");
       return;
       }
    x=fpbn(wordbuf);
    if(x== -1)
       {
       bprintf("They aren't playing\n");
       return;
       }
       if(Player(x).test_flag(1))
       {
       	bprintf("You can't exorcise them, they dont want to be exorcised\n");
       	return;
       	}
    syslog("%s exorcised %s",globme,Player(x).name);
    dumpstuff(x,Player(x).location);
    user.send_message(Message(Player(x).name,globme,-10010,curch,"");
    Player(x).remove()
    }
 
 givecom()
    {
    auto long  a,b;
    auto long  c,d;
    extern char wordbuf[];
    if(brkword()== -1)
       {
       bprintf("Give what to who ?\n");
       return;
       }
    if(fpbn(wordbuf)!= -1) goto obfrst;
    a=fobna(wordbuf);
    if(a== -1)
       {
       bprintf("You aren't carrying that\n");
       return(0);
       }
    /* a = item giving */
    if(brkword()== -1)
       {
       bprintf("But to who ?\n");
       return;
       }
    if(!strcmp(wordbuf,"to"))
       {
       if(brkword()== -1)
          {
          bprintf("But to who ?\n");
          return;
          }
       }
    c=fpbn(wordbuf);
    if(c== -1)
       {
       bprintf("I don't know who %s is\n",wordbuf);
       return;
       }
    dogive(a,c);
    return;
    obfrst:/* a=player */
    a=fpbn(wordbuf);
    if(a== -1)
       {
       bprintf("Who is %s\n",wordbuf);
       return;
       }
    if(brkword()== -1)
       {
       bprintf("Give them what ?\n");
       return;
       }
    c=fobna(wordbuf);
    if(c== -1)
       {
       bprintf("You are not carrying that\n");
       return;
       }
    dogive(c,a);
    }
 
 dogive(ob,pl)
    {
    long  x;
    auto z[32];
    extern char globme[];
    extern long my_lev,curch;
    extern long mynum;
    if((my_lev<10)&&(Player(pl).location!=curch))
       {
       bprintf("They are not here\n");
       return;
       }
    if(!iscarrby(ob,mynum))
       {
       bprintf("You are not carrying that\n");
       }
    if(!cancarry(pl))
       {
       bprintf("They can't carry that\n");
       return;
       }
    if((my_lev<10)&&(ob==32))
       {
       bprintf("It doesn't wish to be given away.....\n");
       return;
       }
    Item(ob).location(pl,1);
    sprintf(z,"\001p%s\001 gives you the %s\n",globme,Item(ob).name);
    user.send_message(Message(Player(pl).name,globme,-10011,curch,z);
    return;
    }

 stealcom()
    {
    extern long mynum;
    extern long curch,my_lev;
    extern char wordbuf[];
    long  a,b;
    long  c,d;
    char x[128];
    long e,f;
    extern char globme[];
    char tb[128];
    if(brkword()== -1)
       {
       bprintf("Steal what from who ?\n");
       return;
       }
    strcpy(x,wordbuf);
    if(brkword()== -1)
       {
       bprintf("From who ?\n");
       return;
       }
    if(!strcmp(wordbuf,"from"))
       {
       if(brkword()== -1)
          {
          bprintf("From who ?\n");
          return;
          }
       }
    c=fpbn(wordbuf);
    if(c== -1)
       {
       bprintf("Who is that ?\n");
       return;
       }
    a=fobncb(x,c);
    if(a== -1)
       {
       bprintf("They are not carrying that\n");
       return;
       }
    if((my_lev<10)&&(Player(c).location!=curch))
       {
       bprintf("But they aren't here\n");
       return;
       }
    if(Item(a).carry_flag==2)
       {
       bprintf("They are wearing that\n");
       return;
       }
    if(Player(c).weapon==a)
       {
       bprintf("They have that firmly to hand .. for KILLING people with\n");
       	return;
       }
    if(!cancarry(mynum))
       {
       bprintf("You can't carry any more\n");
       return;
       }
    time(&f);
    srand(f);
    f=randperc();
    e=10+my_lev-Player(c).level;
    e*=5;
    if(f<e)
       {
       sprintf(tb,"\001p%s\001 steals the %s from you !\n",globme,Item(a).name);
       if(f&1){
       	 user.send_message(Message(Player(c).name,globme,-10011,curch,tb);
       	 if(c>15) woundmn(c,0);
       	}
       Item(a).location(mynum,1);
       return;
       }
    else
       {
       bprintf("Your attempt fails\n");
       return;
       }
    }
 
 dosumm(loc)
    {
    char ms[128];
    extern long curch;
    extern char globme[];
    sprintf(ms,"\001s%s\001%s vanishes in a puff of smoke\n\001",globme,globme);
    user.send_message(Message(globme,globme,-10000,curch,ms);
    sprintf(ms,"\001s%s\001%s appears in a puff of smoke\n\001",globme,globme);
    dumpitems();
    curch=loc;
    user.send_message(Message(globme,globme,-10000,curch,ms);
    trapch(curch);
    }
 
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
    extern long cms;
    extern long mynum;
    char ms[128];
    extern char globme[];
    if(!Player(mynum).test_flag(3))
       {
       bprintf("Dum de dum.....\n");
       return;
       }
      
    sprintf(ms,"\001s%s\001%s fades out of reality\n\001",globme,globme);
    user.send_message(Message(globme,globme,-10113,0,ms); /* Info */
    cms= -2;/* CODE NUMBER */
    update(globme);
    pbfr();
    closeworld();
    if(chdir(ROOMS)==-1) bprintf("Warning: Can't CHDIR\n");
    sprintf(ms,"/cs_d/aberstudent/yr2/hy8/.sunbin/emacs");
    system(ms);
    cms= -1;
    openworld();
    if(fpbns(globme)== -1)
       {
       loseme();
       crapup("You have been kicked off");
       }
    sprintf(ms,"\001s%s\001%s re-enters the normal universe\n\001",globme,globme);
    user.send_message(Message(globme,globme,-10113,0,ms);
    rte();
    }
 
 u_system()
    {
    extern long my_lev;
    extern char globme[];
    extern long cms;
    char x[128];
    if(my_lev<10)
       {
       bprintf("You'll have to leave the game first!\n");
       return;
       }
    cms= -2;
    update(globme);
    sprintf(x,"%s%s%s%s%s","\001s",globme,"\001",globme," has dropped into BB\n\001");
    user.send_message(Message(globme,globme,-10113,0,x);
    closeworld();
    system("/cs_d/aberstudent/yr2/iy7/bt");
    openworld();
    cms= -1;
    if(fpbns(globme)== -1)
       {
       loseme();
       crapup("You have been kicked off");
       }
    rte();
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
    loseme();
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
    loseme();
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
    extern long convflg;
    convflg=1;
    bprintf("Type '**' on a line of its own to exit converse mode\n");
    }
 
 shellcom()
    {
    extern long convflg,my_lev;
    if(my_lev<10000)
       {
       bprintf("There is nothing here you can shell\n");
       return;
       }
    convflg=2;
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
       Broadcast(x+1).send(user);
       return;
       }
    else
       {
       sprintf(y,"%s%s%s","** SYSTEM : ",x,"\n\007\007");
       Broadcast(y).send(user);
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
	extern long curch;
	sprintf(y,"%s in %d",globme,curch);
	getreinput(x);
	syslog("Typo by %s : %s",y,x);
}

look_cmd()
{
	int a;
	long brhold;
	extern long brmode;
	extern char wordbuf[];
        extern long curch;
	if(brkword()==-1)
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
        extern long curch;
	if((Item(186).location==curch)&&(Item(186).is_destroyed))
	{
		bprintf("You uncover a stone slab!\n");
		Item(186).create();
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

emptycom()
{
	long a,b;
	extern long numobs;
        extern long mynum;
	char x[81];
	b=ohereandget(&a);
	if(b==-1) return;
	b=0;
	while(b<numobs)
	{
		if(iscontin(b,a))
		{
			Item(b).set_location(mynum,1);
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