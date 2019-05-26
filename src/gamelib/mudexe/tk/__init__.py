"""
AberMUD II   C


This game systems, its code scenario and design
are (C) 1987/88  Alan Cox,Jim Finnis,Richard Acott


This file holds the basic communications routines
"""
import logging
from services.errors import CrapupError, FileServiceError
from services.mud_exe import MudExeServices
from services.world import WorldService
from ..support import Player
from ..weather import is_dark
from .special import special


class Blood:
    fighting = None
    in_fight = None

    @classmethod
    def fighting_with(cls):
        return Player.players[cls.fighting]

    @classmethod
    def stop_fight(cls):
        cls.in_fight = 0
        cls.fighting = None

    @classmethod
    def update(cls, channel):
        if cls.fighting is not None:
            if not cls.fighting_with().exists:
                cls.stop_fight()
            if cls.fighting_with().location != channel:
                cls.stop_fight()
        if cls.in_fight:
            cls.in_fight -= 1


class New1:
    ail_blind = False


class NewUaf:
    score = 0
    level = 0
    strength = 0
    sex = 0


class Parser:
    zapped = False

    tdes = 0
    vdes = False
    rdes = False
    # ades = 0

    debug_mode = 0

    @classmethod
    def clear_des(cls):
        cls.tdes = 0
        cls.rdes = cls.vdes = False


def sendsys(*args):
    logging.debug("sendsys(%s)", args)


def dumpitems(*args):
    logging.debug("dumpitems(%s)", args)


def saveme(*args):
    logging.debug("saveme(%s)", args)


def chksnp(*args):
    logging.debug("chksnp(%s)", args)


def on_timing(*args):
    logging.debug("on_timing(%s)", args)


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

"""


class Talker:
    MODE_SPECIAL = 0
    MODE_GAME = 1

    CONVERSATION_MODE_CMD = 0
    CONVERSATION_MODE_SAY = 1
    CONVERSATION_MODE_TSS = 2

    __PROMPTS = {
        CONVERSATION_MODE_CMD: ">",
        CONVERSATION_MODE_SAY: "\"",
        CONVERSATION_MODE_TSS: "*",
    }

    def __init__(
        self,
        name,
        on_loose=lambda: None,
        get_cmd=lambda: None,
        show_buffer=lambda: None,
    ):
        """

        :param name:
        """
        # Externals
        Player.fill()

        self.on_loose = on_loose
        self.get_cmd = get_cmd
        self.show_buffer = show_buffer

        self.__active = False
        self.__mode = self.MODE_SPECIAL
        self.__conversation_mode = self.CONVERSATION_MODE_CMD
        self.__ready_to_read = False
        self.__last_update = 0
        self.__is_on = False

        self.__name = name
        self.__player_id = None
        self.__message_id = None
        self.__channel = 0

        try:
            with WorldService():
                self.__put_on()
                self.rte()

            self.__message_id = None
            special('.g', self)
        except OverflowError:
            raise CrapupError("\nSorry AberMUD is full at the moment")
        except FileServiceError as e:
            raise CrapupError(e)

        self.__active = True

    @property
    def active(self):
        return self.__active

    @property
    def mode(self):
        return self.__mode

    @property
    def player(self):
        return Player.players[self.__player_id]

    @property
    def prompt(self):
        result = ""
        if Parser.debug_mode:
            result += "#"
        if NewUaf.level > 9:
            result += "----"
        result += self.__PROMPTS.get(self.__conversation_mode, "?")
        if self.player.visible:
            result = "({})".format(result)
        return "\n" + result

    @property
    def __is_updated(self):
        last_message = self.__message_id or 0
        messages = last_message - self.__last_update
        if messages < 0:
            messages = -messages
        return messages < 10

    def __mstoout(self, message):
        """
        Print appropriate stuff from data block

        :param message:
        :return:
        """
        block0, code, text = message
        # if Parser.debug_mode:
        #     bprintf("\n&lt;{}&gt;".format(code))
        # if code < -3:
        #     sysctrl(message, self.__name.lower())
        # else:
        #     bprintf(text)

    def __prepare_cmd(self, work):
        if not work:
            return ""
        if work != "*" and work[0] == "*":
            return work[1:]
        if self.__conversation_mode == self.CONVERSATION_MODE_SAY:
            return "say {}".format(work)
        elif self.__conversation_mode == self.CONVERSATION_MODE_TSS:
            return "tss {}".format(work)
        return work

    def __put_on(self):
        self.__is_on = False
        MudExeServices.post_player(self.__name, self.__channel)
        self.__is_on = True

    def process_cmd(self, cmd):
        with WorldService():
            self.rte()

        if self.__conversation_mode != self.CONVERSATION_MODE_CMD and cmd == "**":
            self.__conversation_mode = self.CONVERSATION_MODE_CMD
            return self.get_cmd()

        cmd = self.__prepare_cmd(cmd)

        if self.mode == self.MODE_GAME:
            gamecom(cmd)
        else:
            special(cmd, self)

        Blood.update(self.__channel)

        return cmd.lower() == ".q"

    def show(self):
        """

        :return:
        """
        # sendmsg(name)
        self.get_cmd()

        if self.__ready_to_read:
            self.rte()
        self.__ready_to_read = False
        WorldService.disconnect()

    def on_time(self):
        with WorldService():
            self.__interrupt = True
            self.rte()
            self.__interrupt = False
            on_timing()

    def loseme(self):
        """

        :return:
        """
        # sig_aloff()
        # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        self.on_loose()

        self.__active = False

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

        if not Parser.zapped:
            saveme()
        chksnp()

    def rte(self):
        try:
            messages = MudExeServices.get_messages(self.__message_id)
            self.__message_id = messages.get('message_id')
            for message in messages.get('messages', []):
                self.__mstoout(message)

            self.update()
            eorte()
            Parser.clear_des()
        except FileServiceError as e:
            raise CrapupError(e)

    def update(self):
        if self.__is_updated:
            return

        MudExeServices.put_position(self.__player_id, self.__message_id)
        self.__last_update = self.__message_id

    def trapch(self, channel):
        """

        :return:
        """
        WorldService.connect()
        self.player.location = channel
        lookin(channel)

    def set_name(self, player):
        """
        Assign Him her etc according to who it is

        :return:
        """
        # if player.gender == player.GENDER_IT:
        #     wd_it = player.name
        #     return
        # elif player.gender == player.GENDER_SHE:
        #     wd_her = player.name
        # else:
        #     wd_him = player.name
        # wd_them = player.name
        pass

    def see_player(self, player):
        """

        :return:
        """
        if player is None:
            return True
        if player.player_id == self.__player_id:
            return True
        if self.player.level < player.visible:
            return False
        if New1.ail_blind:
            return False
        if self.__channel == player.location and is_dark(self):
            return False

        self.set_name(player)
        return True

    def fpbn(self, name):
        player = Player.fpbns(name)
        if player is None:
            return None
        if not self.see_player(player):
            return None
        return player

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
 broad(mesg)
 char *mesg;
    {
extern long rd_qd;
char bk2[256];
long block[128];
self.__ready_to_read = True
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
    long ct;
    closeworld();
    if(New1.ail_blind)
    {
    	bprintf("You are blind... you can't see a thing!\n");
    }
    if(NewUaf.level>9) showname(room);
    un1=openroom(room,"r");
    if (un1!=NULL)
    {
xx1:   xxx=0;
       lodex(un1);
       	if(WeatherServices.get_is_dark(talker.channel))
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
             if(New1.ail_blind) {rewind(un1);New1.ail_blind=0;goto xx1;}
             if(NewUaf.level>9)bprintf("<DEATH ROOM>\n");
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
             if((!New1.ail_blind)&&(!xxx))bprintf("%s\n",str);
          xxx=brmode;
}
          }
       }
    else
       bprintf("\nYou are on channel %d\n",room);
    fclose(un1);
    openworld();
    if(!New1.ail_blind)
    {
	    lisobs();
	    if(self.mode==self.MODE_GAME) lispeople();
    }
    bprintf("\n");
    onlook();
    }
 loodrv()
    {
    lookin(self.__channel);
    }


userwrap()
{
extern char globme[];
extern long iamon;
if(fpbns(globme)!= -1) {loseme();syslog("System Wrapup exorcised %s",globme);}
}
"""
