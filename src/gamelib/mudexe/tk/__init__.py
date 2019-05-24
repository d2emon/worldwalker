"""
AberMUD II   C


This game systems, its code scenario and design
are (C) 1987/88  Alan Cox,Jim Finnis,Richard Acott


This file holds the basic communications routines
"""
import logging
from services.errors import CrapupError, FileServiceError
from services.bprintf import BufferService
from services.world import WorldService


class Player:
    maxu = 16
    players = []

    def __init__(self, player_id, name=None, curch=None):
        self.player_id = player_id
        self.__name = name
        self.__loc = curch
        self.__pos = None
        self.__lev = 1
        self.__vis = 0
        self.__str = -1
        self.__wpn = -1
        self.__sex = 0
        self.__helping = None

    @property
    def exists(self):
        return self.__name is not None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def strength(self):
        return self.__str

    @strength.setter
    def strength(self, value):
        self.__str = value

    @property
    def level(self):
        return self.__lev

    @level.setter
    def level(self, value):
        self.__lev = value

    @property
    def location(self):
        return self.__loc

    @location.setter
    def location(self, value):
        self.__loc = value

    @property
    def visible(self):
        return self.__vis

    @visible.setter
    def visible(self, value):
        self.__vis = value

    @property
    def position(self):
        return self.__pos

    @position.setter
    def position(self, value):
        self.__pos = value

    @property
    def weapon(self):
        return self.__wpn

    @weapon.setter
    def weapon(self, value):
        self.__wpn = value

    @property
    def helping(self):
        return self.__helping

    @helping.setter
    def helping(self, value):
        self.__helping = value

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, value):
        self.__sex = value

    @property
    def sex_all(self):
        return self.__sex

    @sex_all.setter
    def sex_all(self, value):
        self.__sex = value

    def remove(self):
        self.__name = None

    @classmethod
    def fill(cls):
        cls.players = [cls(player_id) for player_id in range(cls.maxu)]

    @classmethod
    def find_empty(cls):
        for player_id, player in enumerate(cls.players):
            if not player.exists:
                return player_id
        raise OverflowError()

    def add(self):
        self.players[self.player_id] = self


def sendsys(*args):
    logging.debug("sendsys(%s)", args)


def fpbn(*args):
    logging.debug("fpbn(%s)", args)


def dumpitems(*args):
    logging.debug("dumpitems(%s)", args)


def saveme(*args):
    logging.debug("saveme(%s)", args)


def chksnp(*args):
    logging.debug("chksnp(%s)", args)


def on_timing(*args):
    logging.debug("on_timing(%s)", args)


def mstoout(*args):
    logging.debug("mstoout(%s)", args)


def readmsg(*args):
    logging.debug("readmsg(%s)", args)
    return []


def eorte(*args):
    logging.debug("eorte(%s)", args)


def initme(*args):
    logging.debug("initme(%s)", args)


def randperc(*args):
    logging.debug("randperc(%s)", args)
    return 1


def lookin(*args):
    logging.debug("lookin(%s)", args)


def set_progname(*args):
    logging.debug("set_progname(%s)", args)


def gamecom(*args):
    logging.debug("gamecom(%s)", args)


def btmscr(*args):
    logging.debug("btmscr(%s)", args)


"""
Data format for mud packets

Sector 0
[64 words]
0   Current first message pointer
1   Control Word
Sectors 1-n  in pairs ie [128 words]

[channel][controlword][text data]

[controlword]
0 = Text
- 1 = general request
"""


"""
vcpy(dest,offd,source,offs,len)
long *dest,*source;
long offd,offs,len;
    {
    long c;
    c=0;
    while(c<len)
       {
       dest[c+offd]=source[c+offs];
       c++;
       }
    }

 mstoout(block,name)
 long *block;char *name;
    {
    extern long debug_mode;
    char luser[40];
    char *x;
    x=(char *)block;
    /* Print appropriate stuff from data block */
    strcpy(luser,name);lowercase(luser);
if(debug_mode)    bprintf("\n<%d>",block[1]);
    if (block[1]<-3) sysctrl(block,luser);
    else
       bprintf("%s", (x+2*sizeof(long)));
    }

 send2(block)
 long *block;
    {
    FILE * unit;
    long number;
    long inpbk[128];
    extern char globme[];
    extern char *echoback;
    	unit=openworld();
    if (unit<0) {loseme();crapup("\nAberMUD: FILE_ACCESS : Access failed\n");}
    sec_read(unit,inpbk,0,64);
    number=2*inpbk[1]-inpbk[0];inpbk[1]++;
    sec_write(unit,block,number,128);
    sec_write(unit,inpbk,0,64);
    if (number>=199) cleanup(inpbk);
    if(number>=199) longwthr();
    }

 readmsg(channel,block,num)
 long channel;
 long *block;
 int num;
    {
    long buff[64],actnum;
    sec_read(channel,buff,0,64);
    actnum=num*2-buff[0];
    sec_read(channel,block,actnum,128);
    }
"""


class Talker:
    def __init__(
        self,
        name,
        on_loose=lambda: None,
        on_before_buffer=lambda: None,
        on_after_buffer=lambda: None,
        on_top=lambda: None,
        on_bottom=lambda: None,
    ):
        """

        :param name:
        """
        self.on_loose = on_loose
        self.on_before_buffer = on_before_buffer
        self.on_after_buffer = on_after_buffer
        self.on_top = on_top
        self.on_bottom = on_bottom

        self.__interrupt = False

        self.__i_setup = False
        # __oddcat = 0
        # __talkfl = 0

        self.__curch = 0

        self.__name = name
        self.__curmode = 0
        # __meall = 0

        # __gurum = 0
        self.__convflg = 0

        self.__fl_com = None

        self.__rd_qd = False

        # __dsdb = 0
        # __moni = 0

        # __bound = 0;
        # __tmpimu = 0;
        # __* echoback = "*e";
        # __* tmpwiz = "."; / *Illegal name so natural immunes are ungettable! * /

        self.__mynum = 0

        self.__lasup = 0

        self.__iamon = False

        # Externals
        Player.fill()
        self.__zapped = None
        self.__vdes = None
        self.__tdes = None
        self.__rdes = None
        self.__my_str = 0
        self.__my_lev = 0
        self.__my_sex = 0
        self.__debug_mode = None
        self.__fighting = None
        self.__in_fight = None

        self.__buffer_id = BufferService.post_new_buffer()
        self.__cms = None

        try:
            with WorldService():
                self.putmeon()
                self.rte()
        except OverflowError:
            raise CrapupError("Sorry AberMUD is full at the moment")
        except FileServiceError:
            raise CrapupError("Sorry AberMUD is currently unavailable")

        self.__cms = None
        self.special('.g')
        self.i_setup = True

    @property
    def player(self):
        return Player.players[self.__mynum]

    def __before_prompt(self):
        self.pbfr()

    def __after_prompt(self):
        if self.__rd_qd:
            self.rte()
        self.__rd_qd = False
        WorldService.disconnect()

        self.pbfr()

    def __sendmsg(self):
        """

        :return:
        """
        def nadj(cmd):
            if self.__curmode == 1:
                gamecom(cmd)
            else:
                if cmd and cmd != ".Q" and cmd != ".q":
                    self.special(cmd)

            if self.__fighting is not None:
                if not Player.players[self.__fighting].exists:
                    self.__in_fight = 0
                    self.__fighting = None
                if Player.players[self.__fighting].location != self.__curch:
                    self.__in_fight = 0
                    self.__fighting = None

            if self.__in_fight:
                self.__in_fight -= 1

            return cmd == ".Q" or cmd == ".q"

        self.pbfr()

        self.on_bottom()
        # if self.__tty == 4:
        #     btmscr()

        prmpt = "\n"
        if self.player.visible:
            prmpt += "("
        if self.__debug_mode:
            prmpt += "#"
        if self.__my_lev > 9:
            prmpt += "----"
        if self.__convflg == 0:
            prmpt += ">"
        elif self.__convflg == 1:
            prmpt += "\""
        elif self.__convflg == 2:
            prmpt += "*"
        else:
            prmpt += "?"
        if self.player.visible:
            prmpt += ")"

        self.pbfr()

        if self.player.visible > 9999:
            set_progname(0, "-csh")
            work = ""
        else:
            work = "   --}}----- ABERMUD -----{{--     Playing as {}".format(self.__name)
        if self.player.visible == 0:
            set_progname(0, work)

        work = input(prmpt)
        # sig_alon()
        # key_input(prmpt, 80)
        # sig_aloff()
        # work = self.__key_buff

        self.on_top()
        # if self.__tty == 4:
        #     topscr()

        BufferService.post_buffer(self.__buffer_id, "<l>{}\n</l>".format(work))

        with WorldService():
            self.rte()

        if self.__convflg and work == "**":
            self.__convflg = 0
            return self.__sendmsg()

        if not work:
            return nadj("")

        if work != "*" and work[0] == "*":
            return nadj(work[1:])

        if self.__convflg:
            if self.__convflg == 1:
                return nadj("say {}".format(work))
            else:
                return nadj("tss {}".format(work))

        return nadj(work)

    def show(self):
        """

        :return:
        """
        self.__before_prompt()
        self.__sendmsg()
        self.__after_prompt()

    def on_time(self):
        with WorldService():
            self.__interrupt = True
            self.rte()
            self.__interrupt = False
            on_timing()

    def is_dirty(self):
        return BufferService.get_dirty(self.__buffer_id)

    def pbfr(self, is_finished=True):
        self.on_before_buffer()

        WorldService.disconnect()

        logging.debug("%s:\tpbfr()", self.__buffer_id)
        print(BufferService.get_buffer(self.__buffer_id, is_finished))

        self.on_after_buffer()

    def putmeon(self):
        """

        :return:
        """
        self.__iamon = False

        WorldService.connect()
        if fpbn(self.__name) is not None:
            raise CrapupError("You are already on the system - you may only be on once at a time")

        self.__mynum = Player.find_empty()
        if self.__mynum >= Player.maxu:
            raise OverflowError()

        Player(self.__mynum, self.__name, self.__curch).add()

        self.__iamon = True

    def loseme(self):
        """

        :return:
        """
        # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        self.on_loose()

        self.i_setup = False

        with WorldService():
            dumpitems()
            if self.player.visible < 10000:
                sendsys(
                    self.__name,
                    self.__name,
                    -10113,
                    0,
                    "{} has departed from AberMUDII\n".format(self.__name),
                )
            self.player.remove()

        if not self.__zapped:
            saveme()
        chksnp()

    def rte(self):
        """

        :return:
        """
        try:
            unit = WorldService.connect()
            self.__fl_com = unit

            last_message = WorldService.get_last_message_id()
            self.__cms = self.__cms or last_message
            for ct in range(self.__cms, last_message):
                block = readmsg(unit, ct)
                mstoout(block, self.__name)
            self.__cms = last_message

            self.update()
            eorte()
            self.__rdes = self.__tdes = self.__vdes = 0

        except FileServiceError:
            raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")

    def update(self):
        """

        :return:
        """
        if self.__cms is None:
            xp = - self.__lasup
        else:
            xp = self.__cms - self.__lasup

        if xp < 0:
            xp = -xp

        if xp < 10:
            return

        WorldService.connect()
        self.player.position = self.__cms
        self.__lasup = self.__cms

    def special(self, code):
        """

        :param code:
        :return:
        """
        bk = code.lower()
        if bk[0] != ".":
            return False

        ch = bk[1:]
        if ch == "g":
            self.__curmode = 1
            self.__curch = 5
            initme()
            WorldService.connect()

            self.player.strength = self.__my_str
            self.player.level = self.__my_lev
            if self.__my_lev < 10000:
                self.player.visible = 0
            else:
                self.player.visible = 10000
            self.player.weapon = None
            self.player.sex_all = self.__my_sex
            self.player.helping = None

            xy = "<s user=\"{user}\">{user}  has entered the game\n</s>".format(user=self.__name)
            sendsys(
                self.__name,
                self.__name,
                -10113,
                self.__curch,
                "<s user=\"{user}\">[ {user}  has entered the game ]\n</s>".format(user=self.__name),
            )
            self.rte()
            if randperc() <= 50:
                self.__curch = -183
            self.trapch(self.__curch)
            sendsys(
                self.__name,
                self.__name,
                -10000,
                self.__curch,
                xy,
            )
        else:
            print("\nUnknown . option\n")
        return True

    def trapch(self, channel):
        """

        :return:
        """
        WorldService.connect()
        self.player.location = channel
        lookin(channel)


"""
 cleanup(inpbk)
 long *inpbk;
    {
    FILE * unit;
    long buff[128],ct,work,*bk;
    unit=openworld();
    bk=(long *)malloc(1280*sizeof(long));
    sec_read(unit,bk,101,1280);sec_write(unit,bk,1,1280);
    sec_read(unit,bk,121,1280);sec_write(unit,bk,21,1280);
    sec_read(unit,bk,141,1280);sec_write(unit,bk,41,1280);
    sec_read(unit,bk,161,1280);sec_write(unit,bk,61,1280);
    sec_read(unit,bk,181,1280);sec_write(unit,bk,81,1280);
    free(bk);
    inpbk[0]=inpbk[0]+100;
    sec_write(unit,inpbk,0,64);
    revise(inpbk[0]);
    }
"""

"""


 special(string,name)
 char *string,*name;
    {
    }



 broad(mesg)
 char *mesg;
    {
extern long rd_qd;
char bk2[256];
long block[128];
rd_qd=1;
block[1]= -1;
strcpy(bk2,mesg);
vcpy(block,2,(long *)bk2,0,126);
send2(block);
}

tbroad(message)
char *message;
    {
    broad(message);
    }

 sysctrl(block,luser)
 long *block;
 char *luser;
    {
    gamrcv(block);
    }

 split(block,nam1,nam2,work,luser)
 long *block;
 char *nam1;
 char *nam2;
 char *work;
 char *luser;
    {
    long wkblock[128],a;
    vcpy(wkblock,0,block,2,126);
    vcpy((long *)work,0,block,64,64);
    a=scan(nam1,(char *)wkblock,0,"",".");
    scan(nam2,(char *)wkblock,a+1,"",".");
if((strncmp(nam1,"The ",4)==0)||(strncmp(nam1,"the ",4)==0))
{
if(!strcmp(lowercase(nam1+4),lowercase(luser))) return(1);
}
    return(!strcmp(lowercase(nam1),lowercase(luser)));
    }
"""


"""
 revise(cutoff)
 long cutoff;
    {
    char mess[128];
    long ct;
    FILE *unit;
    unit=openworld();
    ct=0;
    while(ct<16)
       {
       if((pname(ct)[0]!=0)&&(ppos(ct)<cutoff/2)&&(ppos(ct)!=-2))
          {
          sprintf(mess,"%s%s",pname(ct)," has been timed out\n");
          broad(mess);
          dumpstuff(ct,ploc(ct));
          pname(ct)[0]=0;
          }
       ct++;
       }
    }

 lookin(room)
 long room; /* Lords ???? */
    {
    extern char globme[];
    FILE *un1,un2;
    char str[128];
    long xxx;
    extern long brmode;
    extern long curmode;
    extern long ail_blind;
    long ct;
    extern long my_lev;
    closeworld();
    if(ail_blind)
    {
    	bprintf("You are blind... you can't see a thing!\n");
    }
    if(my_lev>9) showname(room);
    un1=openroom(room,"r");
    if (un1!=NULL)
    {
xx1:   xxx=0;
       lodex(un1);
       	if(isdark())
       	{
          		fclose(un1);
          		bprintf("It is dark\n");
                        openworld();
          		onlook();
          		return;
          	}
       while(getstr(un1,str)!=0)
          {
          if(!strcmp(str,"#DIE"))
             {
             if(ail_blind) {rewind(un1);ail_blind=0;goto xx1;}
             if(my_lev>9)bprintf("<DEATH ROOM>\n");
             else
                {
                loseme(globme);
                crapup("bye bye.....\n");
                }
             }
          else
{
if(!strcmp(str,"#NOBR")) brmode=0;
else
             if((!ail_blind)&&(!xxx))bprintf("%s\n",str);
          xxx=brmode;
}
          }
       }
    else
       bprintf("\nYou are on channel %d\n",room);
    fclose(un1);
    openworld();
    if(!ail_blind)
    {
	    lisobs();
	    if(curmode==1) lispeople();
    }
    bprintf("\n");
    onlook();
    }
 loodrv()
    {
    extern long curch;
    lookin(curch);
    }


userwrap()
{
extern char globme[];
extern long iamon;
if(fpbns(globme)!= -1) {loseme();syslog("System Wrapup exorcised %s",globme);}
}
"""
