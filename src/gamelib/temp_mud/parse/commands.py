from ..errors import CommandError, CrapupError

from ..blood import Blood
from ..new1 import resetplayers, woundmn, teletrap
from ..new1.disease import DISEASES
from ..new1.messages import MSG_GLOBAL, MSG_WIZARD, MSG_SHOUT
from ..newuaf import NewUaf
from ..objsys import ObjSys, iscarrby, dumpitems, dumpstuff
from ..opensys import openworld, closeworld
from ..support import Item, Door, Player
from ..syslog import syslog
from ..tk import Tk, trapch, broad
from .messages import Message


def disle3(*args):
    raise NotImplementedError


def saveme(*args):
    raise NotImplementedError


"""
char *verbtxt[]={,
    "laugh",
    "cry","burp","fart","hiccup","grin","smile","wink","snigger","pose","set",
    "pray","storm","rain","sun","snow","goto",

    "wear",
    "remove","put","wave","blizzard","open","close","shut","lock","unlock","force","light",
    "extinguish","where","turn","invisible","visible","pull","press","push","cripple","cure","dumb",
    "change","missile","shock","fireball","translocate","blow","sigh","kiss","hug","slap",
    "tickle","scream","bounce","wiz","stare","exits","crash","sing","grope","spray",
    "groan","moan","directory","yawn","wizlist","in","smoke","deafen","resurrect","log",
    "tss","rmedit","loc","squeeze","users","honeyboard","inumber","update","become","systat",
    "converse","snoop","shell","raw","purr","cuddle","sulk","roll","credits","brief",
    "debug","jump","map","flee","bug","typo","pn","blind","patch","debugmode",
    "pflags","frobnicate","setin","setout","setmin","setmout","emote","dig","empty"
    };
int verbnum[]={
    50,
    51,52,53,54,55,56,57,58,59,60,
    61,62,63,64,65,66,

    100,
    101,102,103,104,105,106,106,107,108,109,110,
    111,112,117,114,115,117,117,117,118,119,120,
    121,122,123,124,125,126,127,128,129,130,
    131,132,133,134,135,136,137,138,139,140,
    141,142,143,144,145,146,147,148,149,150,
    151,152,153,154,155,156,157,158,159,160,
    161,162,163,164,165,166,167,168,169,170,
    171,172,173,174,175,176,177,178,179,180,
    181,182,183,184,185,186,187,188,189
    };
 
 doaction(n)
    {
    if((n>1)&&(n<8)){dodirn(n);return;}
    switch(n)
       {
       case 1:
       case 8:
       case 9:
       case 10:

       case 11:
       case 12:
       case 13:
       case 14:
       case 15:
       case 16:
       case 17:
       case 18:
       case 19:
       case 20:

       case 21:
       case 22:
       case 23:
       case 24:
       case 25:
       case 26:
       case 27:
       case 28:
       case 29:
       case 30:

       case 31:
       case 32:
       case 33:
       case 34:
       case 35:

       case 50:
          laughcom();
          break;

       case 51:
          crycom();
          break;
       case 52:
          burpcom();
          break;
       case 53:
          fartcom();
          break;
       case 54:
          hiccupcom();
          break;
       case 55:
          grincom();
          break;
       case 56:
          smilecom();
          break;
       case 57:
          winkcom();
          break;
       case 58:
          sniggercom();
          break;
       case 59:
          posecom();
          break;
       case 60:
          setcom();
          break;

       case 61:
          praycom();
          break;
       case 62:
          stormcom();
          break;
       case 63:
          raincom();
          break;
       case 64:
          suncom();
          break;
       case 65:
          snowcom();
          break;
       case 66:
          goloccom();
          break;

       case 100:
          wearcom();
          break;

       case 101:
          removecom();
          break;
       case 102:
          putcom();
          break;
       case 103:
          wavecom();
          break;
       case 104:
          blizzardcom();
          break;
       case 105:
          opencom();
          break;
       case 106:
          closecom();
          break;
       case 107:
          lockcom();
          break;
       case 108:
          unlockcom();
          break;
       case 109:
          forcecom();
          break;
       case 110:
          lightcom();
          break;

       case 111:
          extinguishcom();
          break;
       case 112:
          wherecom();
          break;
       case 117:;
       case 113:
          pushcom();
          break;
       case 114:
          inviscom();
          break;
       case 115:
          viscom();
          break;
       case 118:
          cripplecom();
          break;
       case 119:
          curecom();
          break;
       case 120:
          dumbcom();
          break;

       case 121:
          changecom();
          break;
       case 122:
          missilecom();
          break;
       case 123:
          shockcom();
          break;
       case 124:
          fireballcom();
          break;
       case 126:
          blowcom();
          break;
       case 127:
          sighcom();
          break;
       case 128:
          kisscom();
          break;
       case 129:
          hugcom();
          break;
       case 130:
          slapcom();
          break;

       case 131:
          ticklecom();
          break;
       case 132:
          screamcom();
          break;
       case 133:
          bouncecom();
          break;
       case 134:
          wizcom();
          break;
       case 135:
          starecom();
          break;
       case 136:
          exits();
          break;
       case 137:
          crashcom();
          break;
       case 138:
          singcom();
          break;
       case 139:
          if(in_fight) 
             {
             bprintf("Not in a fight!\n");break;
             }
          gropecom();
          break;
       case 140:
          spraycom();
          break;

       case 141:
          groancom();
          break;
       case 142:
          moancom();
          break;
       case 143:
          dircom();
          break;
       case 144:
          yawncom();
          break;
       case 145:
          wizlist();
          break;
       case 146:
          incom();
          break;
       case 147:
          lightcom();
          break;
       case 148:
          deafcom();
          break;
       case 149:
          ressurcom();
          break;
       case 150:
          logcom();
          break;

       case 151:
          tsscom();
          break;
       case 152:
          rmeditcom();
          break;
       case 153:
          loccom();
          break;
       case 154:
          squeezecom();
          break;
       case 155:
          usercom();
          break;
       case 156:
          u_system();
          break;
       case 157:
          inumcom();
          break;
       case 158:
          updcom();
          break;
       case 159:
          becom();
          break;
       case 160:
          systat();
          break;

       case 161:
          convcom();
          break;
       case 162:
          snoopcom();
          break;
       case 163:
          shellcom();
          break;
       case 164:
          rawcom();
          break;
       case 165:
          purrcom();
          break;
       case 166:
          cuddlecom();
          break;
       case 167:
          sulkcom();
          break;
       case 168:
          rollcom();
          break;
       case 169:
          bprintf("\001f%s\001",CREDITS);
          break;
       case 170:
          brmode=!brmode;
          break;

       case 171:
          debugcom();
          break;
       case 172:
          jumpcom();
          break;
       case 173:
          bprintf("Your adventurers automatic monster detecting radar, and long range\n");
          bprintf("mapping kit, is, sadly, out of order.\n");break;
       case 174:
          if(!in_fight)
             {
             dogocom();
             break;
             }
          else
             {
             char ar[120];
             if(iscarrby(32,mynum)) 
                {
                bprintf("The sword won't let you!!!!\n");
                break;
                }
             sprintf(ar,"\001c%s\001 drops everything in a frantic attempt to escape\n",globme);
             Message(globme,globme,-10000,curch,ar).send();
             Message(globme,globme,-20000,curch,"").send();
             my_sco-=my_sco/33; /* loose 3% */
             parser.calibme();
             in_fight=0;
             on_flee_event();
             dogocom();
             break;
             }
       case 175:
          bugcom();
          break;
       case 176:
          typocom();
          break;
       case 177:
          pncom();
          break;
       case 178:
          blindcom();
          break;
       case 179:
          edit_world();
          break;
       case 180:
          if(ptstflg(mynum,4)) debug_mode=1-debug_mode;
          break;

       case 181:
          setpflags();
          break;
       case 182:
          frobnicate();
          break;
       case 183:
          setincom();
          break;
       case 184:
          setoutcom();
          break;
       case 185:
          setmincom();
          break;
       case 186:
          setmoutcom();
          break;
       case 187:
          emotecom();
          break;
       case 188:
          digcom();
          break;
       case 189:
          emptycom();
          break;

       default:
          if(my_lev>9999)bprintf("Sorry not written yet[COMREF %d]\n",n);
          else bprintf("I don't know that verb.\n");
          break;
       }
    }

"""




class Take(Command):
    item_id = 9
    verbs = "get", "take",

    @classmethod
    def action(cls, parser):
        # getobj()
        pass


class Drop(Command):
    item_id = 10
    verbs = "drop",

    @classmethod
    def action(cls, parser):
        # dropitem()
        pass


class Look(Command):
    item_id = 11
    verbs = "look",

    @classmethod
    def action(cls, parser):
        #           look_cmd();
        pass


class Inventory(Command):
    item_id = 12
    verbs = "i", "inv", "inventory"

    @classmethod
    def action(cls, parser):
        #           inventory();
        pass


class Who(Command):
    item_id = 13
    verbs = "who",

    @classmethod
    def action(cls, parser):
        #           whocom();
        pass


class Save(Command):
    item_id = 21
    verbs = "save",

    @classmethod
    def action(cls, parser):
        #   saveme();
        pass


class Score(Command):
    item_id = 22
    verbs = "score",

    @classmethod
    def action(cls, parser):
        if NewUaf.my_lev == 1:
            yield "Your strength is {}\n".format(NewUaf.my_str)
            return
        yield "Your strength is {}(from {}),Your score is {}\nThis ranks you as {} ".format(
            NewUaf.my_str,
            50 + 8 * NewUaf.my_lev,
            NewUaf.my_sco,
            Tk.globme
        )
        disle3(NewUaf.my_lev, NewUaf.my_sex)


class Exorcise(Command):
    item_id = 23
    verbs = "exorcise",

    @classmethod
    def action(cls, parser):
        if NewUaf.my_lev < 10:
            raise CommandError("No chance....\n")
        word = parser.brkword
        if word is None:
            raise CommandError("Exorcise who ?\n")
        player = Player.fpbn(word)
        if player is None:
            raise CommandError("They aren't playing\n")
        if player.tstflg(1):
            raise CommandError("You can't exorcise them, they dont want to be exorcised\n")
        syslog("{} exorcised {}".format(Tk.globme, player.name))
        dumpstuff(player, player.location)
        Message(
            player,
            Tk,
            -10010,
            Tk.curch,
            ''
        ).send()
        player.name = None
        pass


class Give(Command):
    item_id = 24
    verbs = "give",

    @classmethod
    def __player_item(cls, parser, player):
        word = parser.brkword
        if word is None:
            raise CommandError("Give them what ?\n")
        item = Item.fobna(word)
        if item is None:
            raise CommandError("You are not carrying that\n")
        return item, player

    @classmethod
    def __item_player(cls, parser, item):
        word = parser.brkword
        if word is None:
            raise CommandError("But to who ?\n")
        if word == "to":
            word = parser.brkword
            if word is None:
                raise CommandError("But to who ?\n")

        player = Player.fpbn(word)
        if player is None:
            raise CommandError("I don't know who {} is\n".format(word))
        return item, player

    @classmethod
    def action(cls, parser):
        word = parser.brkword
        if word is None:
            raise CommandError("Give what to who ?\n")

        player = Player.fpbn(word)
        if player is None:
            item = Item.fobna(word)
            if item is None:
                raise CommandError("You aren't carrying that\n")

            return parser.dogive(*cls.__item_player(parser, item))
        else:
            return parser.dogive(*cls.__player_item(parser, player))


class Steal(Command):
    item_id = 25
    verbs = "steal", "pinch",

    @classmethod
    def action(cls, parser):
        word = parser.brkword
        if word is None:
            raise CommandError("Steal what from who ?\n")
        x = word

        word = parser.brkword
        if word is None:
            raise CommandError("From who ?\n")
        if word == "from":
            word = parser.brkword
            if word is None:
                raise CommandError("From who ?\n")
        player = Player.fpbn(word)
        if player is None:
            raise CommandError("Who is that ?\n")
        item = Item.fobncb(x, player)
        if item is None:
            raise CommandError("They are not carrying that\n")
        if NewUaf.my_lev < 10 and player.location != Tk.curch:
            raise CommandError("But they aren't here\n")
        if item.carry_flag == 2:
            raise CommandError("They are wearing that\n")
        if player.weapon == item:
            raise CommandError("They have that firmly to hand .. for KILLING people with\n")
        if not Player(Tk.mynum).can_carry:
            raise CommandError("You can't carry any more\n")

        f = time()
        srand(f)
        f = randperc()
        e = 10 + NewUaf.my_lev - player.level
        e *= 5
        if f >= e:
            raise CommandError("Your attempt fails\n")
        if f & 1:
            Message(
                player,
                Tk,
                -10011,
                Tk.curch,
                "\001p{}\001 steals the {} from you !\n".format(Tk.globme, item.name),
            ).send()
            if player.player_id > 15:
                woundmn(player, 0)
        item.setoloc(Tk.mynum, 1)


class Levels(Command):
    item_id = 26
    verbs = "levels",

    @classmethod
    def action(cls, parser):
        #   levcom();
        pass


class Help(Command):
    item_id = 27
    verbs = "help",

    @classmethod
    def action(cls, parser):
        #   helpcom();
        pass


class Values(Command):
    item_id = 28
    verbs = "value",

    @classmethod
    def action(cls, parser):
        #   valuecom();
        pass


class Stats(Command):
    item_id = 29
    verbs = "stats",

    @classmethod
    def action(cls, parser):
        #   stacom();
        pass


class Examine(Command):
    item_id = 30
    verbs = "examine", "read",

    @classmethod
    def action(cls, parser):
        #   examcom();
        pass


class DeletePlayer(Command):
    item_id = 31
    verbs = "delete",

    @classmethod
    def action(cls, parser):
        #             delcom();
        pass


class Password(Command):
    item_id = 32
    verbs = "pass", "password",

    @classmethod
    def action(cls, parser):
        #           passcom();
        pass


class Summon(Command):
    item_id = 33
    verbs = "summon",

    @classmethod
    def action(cls, parser):
        #           sumcom();
        pass


class Weapon(Command):
    item_id = 34
    verbs = "weapon", "wield"

    @classmethod
    def action(cls, parser):
        #           weapcom();
        pass


class Kill(Command):
    item_id = 35
    verbs = "shoot", "kill", "hit", "fire", "launch", "smash", "break", "strike"

    @classmethod
    def action(cls, parser):
        #           killcom();
        pass


EXITS = North, East, South, West, Up, Down

COMMANDS = (
    Go, North, East, South, West, Up, Down, Quit, Take, Drop,
    Look, Inventory, Who, Reset, Zap, Eat, Play, Shout, Say, Tell,
    Save, Score, Exorcise, Give, Steal, Levels, Help, Values, Stats, Examine,
    DeletePlayer, Password, Summon, Weapon, Kill,
)
