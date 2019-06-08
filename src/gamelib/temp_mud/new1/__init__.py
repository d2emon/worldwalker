"""
Extensions section 1
"""
from ..magic import randperc
from ..newuaf import NewUaf
from ..objsys import ObjSys, dumpstuff, iscarrby
from ..parse.messages import Message
from ..support import Item, Player
from ..tk import Tk, trapch
from .disease import Diseases
from .messages import MSG_GLOBAL, MSG_WIZARD, MSG_WOUND
from .utils import get_item


class PlayerData:
    def __init__(self, name, location, strength, sex, level):
        self.name = name
        self.location = location
        self.strength = strength
        self.sex = sex
        self.level = level


SCALES = {
    1: 2,
    2: 3,
    3: 3,
    4: 4,
    5: 4,
    6: 5,
    7: 6,
}


MOBILES = [
    PlayerData("The Wraith", -1077, 60, 0, -2),
    PlayerData("Shazareth", -1080, 99, 0, -30),
    PlayerData("Bomber", -308, 50, 0, -10),
    PlayerData("Owin", -311, 50, 0, -11),
    PlayerData("Glowin", -318, 50, 0, -12),
    PlayerData("Smythe", -320, 50, 0, -13),
    PlayerData("Dio", -332, 50, 0, -14),
    PlayerData("The Dragon", -326, 500, 0, -2),
    PlayerData("The Zombie", -639, 20, 0, -2),
    PlayerData("The Golem", -1056, 90, 0, -2),

    PlayerData("The Haggis", -341, 50, 0, -2),
    PlayerData("The Piper", -630, 50, 0, -2),
    PlayerData("The Rat", -1064, 20, 0, -2),
    PlayerData("The Ghoul", -129, 40, 0, -2),
    PlayerData("The Figure", -130, 90, 0, -2),
    PlayerData("The Ogre", -144, 40, 0, -2),
    PlayerData("Riatha", -165, 50, 0, -31),
    PlayerData("The Yeti", -173, 80, 0, -2),
    PlayerData("The Guardian", -197, 50, 0, -2),
    PlayerData("Prave", -201, 60, 0, -400),

    PlayerData("Wraith", -350, 60, 0, -2),
    PlayerData("Bath", -1, 70, 0, -401),
    PlayerData("Ronnie", -809, 40, 0, -402),
    PlayerData("The Mary", -1, 50, 0, -403),
    PlayerData("The Cookie", -126, 70, 0, -404),
    PlayerData("MSDOS", -1, 50, 0, -405),
    PlayerData("The Devil", -1, 70, 0, -2),
    PlayerData("The Copper", -1, 40, 0, -2),
]


def tscale():
    players = len(list(filter(lambda player: len(player.name) > 0, [Player(b) for b in range(16)])))
    return SCALES.get(players, 7)


def woundmn(enemy, damage):
    new_strength = enemy.strength - damage
    enemy.strength = new_strength

    if new_strength >= 0:
        return mhitplayer(enemy)

    dumpstuff(enemy, enemy.location)
    Message(
        None,
        None,
        MSG_GLOBAL,
        enemy.location,
        "{} has just died\n".format(enemy.name),
    ).send()
    enemy.name = ""
    Message(
        None,
        None,
        MSG_WIZARD,
        enemy.location,
        "[ {} has just died ]\n".format(enemy.name),
    ).send()


def mhitplayer(enemy):
    if enemy.location != user.location_id:
        return
    if enemy.player_id < 0 or enemy.player_id > 47:
        return
    roll = randperc()
    to_hit = 3 * (15 - NewUaf.my_lev) + 20
    if Item(89).is_worn_by(Tk.mynum) or Item(113).is_worn_by(Tk.mynum) or Item(114).is_worn_by(Tk.mynum):
        to_hit -= 10
    if roll < to_hit:
        data = [
            enemy,
            randperc() % enemy.damage,
            -1,
        ]
    else:
        data = [
            enemy,
            -1,
            -1,
        ]
    Message(
        Tk,
        enemy,
        MSG_WOUND,
        enemy.location,
        data,
    ).send()


def resetplayers():
    for mobile_id, mobile in MOBILES:
        player = Player(mobile_id + 16)
        player.name = mobile.name
        player.location = mobile.location
        player.strength = mobile.strength
        player.sex = mobile.sex
        player.weapon = None
        player.visible = 0
        player.level = mobile.level
    for a in range(35, 48):
        Player(a).name = ""


def teletrap(new_channel):
    Message(
        Tk,
        Tk,
        MSG_GLOBAL,
        user.location_id,
        "\001s{name}\001{name} has left.\n\001".format(name=Tk.globme),
    ).send()
    user.location_id = new_channel
    Message(
        Tk,
        Tk,
        MSG_GLOBAL,
        user.location_id,
        "\001s{name}\001{name} has arrived.\n\001".format(name=Tk.globme),
    ).send()
    trapch(user.location_id)


def on_flee_event():
    for item_id in range(ObjSys.numobs):
        item = Item(item_id)
        if iscarrby(item_id, Tk.mynum) and not item.is_worn_by(Tk.mynum):
            item.set_location(Player(Tk.mynum).location, 0)


"""
struct player_res
{
	char *p_name;
	long p_loc;
	long p_str;
	long p_sex;
	long p_lev;
};

typedef struct player_res PLAYER;

 /*
 Extensions section 1
 */

#include <stdio.h>

extern FILE * openuaf();
extern FILE * openlock();
extern FILE * openroom();
extern char globme[];
extern char wordbuf[];
 
 bouncecom()
    {
    sillycom("\001s%s\001%s bounces around\n\001");
    bprintf("B O I N G !!!!\n");
    }
 
 sighcom()
    {
    if(chkdumb()) return;
    sillycom("\001P%s\001\001d sighs loudly\n\001");
    bprintf("You sigh\n");
    }
 
 screamcom()
    {
    if(chkdumb()) return;
    sillycom("\001P%s\001\001d screams loudly\n\001");
    bprintf("ARRRGGGGHHHHHHHHHHHH!!!!!!\n");
    }
 
 /* Door is 6 panel 49
 */
 
 ohereandget(onm)
 long *onm;
    {
    long b;
    extern char wordbuf[];
    if(brkword()==-1)
       {
       bprintf("Tell me more ?\n");
       return(-1);
       }
    openworld();
    *onm=fobna(wordbuf);
    if(*onm==-1)
       {
       bprintf("There isn't one of those here\n");
       return(-1);
       }
    return(1);
    }
 
 state(ob)
    {
    extern long objinfo[];
    return(objinfo[4*ob+1]);
    }
 
 
 opencom()
    {
    extern long mynum;
    long a,b;
    b=ohereandget(&a);
    if(b==-1) return;
    switch(a)
       {
       case 21:if(state(21)==0) bprintf("It is\n");
     else bprintf("It seems to be magically closed\n");
break;
       case 1:
          if(state(1)==1)
             {
             bprintf("It is!\n");
             }
          else
             {
             setstate(1,1);
             bprintf("The Umbrella Opens\n");
             }
          break;
       case 20:
          bprintf("You can't shift the door from this side!!!!\n");break;
       default:
          if(Item(a).test_bit(2)==0)
             {
             bprintf("You can't open that\n");
             return;
             }
          if(state(a)==0)
             {
             bprintf("It already is\n");
             return;
             }
          if(state(a)==2)
             {
             bprintf("It's locked!\n");
             return;
             }
          setstate(a,0);bprintf("Ok\n");
 
          }
    }
 
 setstate(o,v)
    {
    extern long objinfo[];
    objinfo[4*o+1]=v;
    if(Item(o).test_bit(1)) objinfo[4*(o^1)+1]=v;
 
    }
 
 closecom()
    {
    long a,b;
    b=ohereandget(&a);
    if(b==-1) return;
    switch(a)
       {
       case 1:
          if(state(1)==0) bprintf("It is closed, silly!\n");
          else
             {
             bprintf("Ok\n");
             setstate(1,0);
             }
             break;
       default:
          if(Item(a).test_bit(2)==0)
             {
             bprintf("You can't close that\n");
             return;
             }
          if(state(a)!=0)
             {
             bprintf("It is open already\n");
             return;
             }
          setstate(a,1);
          bprintf("Ok\n");
          }
    }
 
 lockcom()
    {
    long a,b;
    extern long mynum;
    b=ohereandget(&a);
    if(b==-1) return;
    if(!user.has_any([
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 1,
    0, 0, 0, 0,
]))
       {
       bprintf("You haven't got a key\n");
       return;
       }
    switch(a)
       {
       default:
          if(!Item(a).test_bit(3))
             {
             bprintf("You can't lock that!\n");
             return;
             }
          if(state(a)==2)
             {
             bprintf("It's already locked\n");
             return;
             }
          setstate(a,2);
          bprintf("Ok\n");
          }
    }
 
 unlockcom()
    {
    long a,b;
    extern long mynum;
    b=ohereandget(&a);
    if(b==-1) return;
    if(!user.has_any([
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 1,
    0, 0, 0, 0,
]))
       {
       bprintf("You have no keys\n");
       return;
       }
    switch(a)
       {
       default:
          if(!Item(a).test_bit(3))
             {
             bprintf("You can't unlock that\n");
             return;
             }
          if(state(a)!=2)
             {
             bprintf("Its not locked!\n");
             return;
             }
          printf("Ok...\n");
          setstate(a,1);
          return;
          }
    }
 
 
 wavecom()
    {
    long a,b;
    b=ohereandget(&a);
    if(b==-1) return;
    switch(a)
       {
       case 136:
          if((state(151)==1)&&(Item(151).location==user.location_id))
             {
             setstate(150,0);
             bprintf("The drawbridge is lowered!\n");
             return;
             }
break ;
       case 158:
          bprintf("You are teleported!\n");
          teletrap(-114);
          return;
          }
    bprintf("Nothing happens\n");
    }
 
 blowcom()
    {
    extern long my_sco;
    long a,b;
    b=ohereandget(&a);
    if(b== -1) return;
    bprintf("You can't blow that\n");
    }
 
 
 putcom()
    {
    long a,b;
    extern long my_sco;
    char ar[128];
    extern char wordbuf[];
    long c;
    b=ohereandget(&a);
    if(b== -1) return;
    if(brkword()== -1)
       {
       bprintf("where ?\n");
       return;
       }
    if((!strcmp(wordbuf,"on"))||(!strcmp(wordbuf,"in")))
       {
       if(brkword()== -1)
          {
          bprintf("What ?\n");
          return;
          }
       }
    c=fobna(wordbuf);
    if(c== -1)
       {
       bprintf("There isn't one of those here.\n");
       return;
       }
    if(c==10)
       {
       if((a<4)||(a>6))
          {
          bprintf("You can't do that\n");
          return;
          }
       if(state(10)!=2)
          {
          bprintf("There is already a candle in it!\n");
          return;
          }
       bprintf("The candle fixes firmly into the candlestick\n");
       my_sco+=50;
       destroy(a);
       Item(10).set_byte(1,a);
       Item(10).set_bit(9);
       Item(10).set_bit(10);
       if(Item(a).test_bit(13))
          {
          Item(10).set_bit(13);
          setstate(10,0);
          return;
          }
       else
          {
          setstate(10,1);
          Item(10).clear_bit(13);
          }
       return;
       }
    if(c==137)
       {
       if(state(c)==0)
          {
          Item(a).set_location(-162,0);
          bprintf("ok\n");
	  return;
          }
       destroy(a);
       bprintf("It dissappears with a fizzle into the slime\n");
       if(a==108)
          {
          bprintf("The soap dissolves the slime away!\n");
          setstate(137,0);
          }
       return;
       }
    if(c==193)
	{
		bprintf("You can't do that, the chute leads up from here!\n");
		return;
	}
    if(c==192)
    {
    	if(a==32)
    	{
    		bprintf("You can't let go of it!\n");
    		return;
    	}
    	bprintf("It vanishes down the chute....\n");
    	sprintf(ar,"The %s comes out of the chute!\n",Item(a).name);
    	user.send_message("","",-10000,Item(193).location,ar);
    	Item(a).set_location(Item(193).location, 0);
    	return;
    }
    	
    if(c==23)
       {
       if((a==19)&&(state(21)==1))
          {
          bprintf("The door clicks open!\n");
          setstate(20,0);
          return;
          }
       bprintf("Nothing happens\n");
       return;
       }
    if(c==a)
    {
    	bprintf("What do you think this is, the goon show ?\n");
	return;
    }
    if(Item(c).test_bit(14)==0) {bprintf("You can't do that\n");return;}
    if(state(c)!=0){bprintf("That's not open\n");return;}
    if(Item(a).flannel)
    {
    	bprintf("You can't take that !\n");
    	return;
    }
    if(dragget()) return;
    if(a==32)
    {
    	bprintf("You can't let go of it!\n");
    	return;
    }
    Item(a).set_location(c,3);
    bprintf("Ok.\n");
    sprintf(ar,"\001D%s\001\001c puts the %s in the %s.\n\001",globme,Item(a).name,Item(c).name);
    user.send_message(globme,globme,-10000,user.location_id,ar);
    if(Item(a).test_bit(12)) setstate(a,0);
    if(user.location_id==-1081) 
    {
	setstate(20,1);
	bprintf("The door clicks shut....\n");
    }    
}
 
 lightcom()
    {
    extern long mynum;
    long a,b;
    b=ohereandget(&a);
    if(b== -1) return;
    if(!user.has_any([
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 1, 0, 0,
]))
       {
       bprintf("You have nothing to light things from\n");
       return;
       }
    switch(a)
       {
       default:
          if(!Item(a).test_bit(9))
             {
             bprintf("You can't light that!\n");
             return;
             }
          if(state(a)==0)
             {
             bprintf("It is lit\n");
             return;
             }
          setstate(a,0);
          Item(a).set_bit(13);
          bprintf("Ok\n");
          }
    }
 
 extinguishcom()
    {
    long a,b;
    b=ohereandget(&a);
    if(b== -1) return;
    switch(a)
       {
       default:
          if(!Item(a).test_bit(13))
             {
             bprintf("That isn't lit\n");
             return;
             }
          if(!Item(a).test_bit(10))
             {
             bprintf("You can't extinguish that!\n");
             return;
             }
          setstate(a,1);
          Item(a).clear_bit(13);
          bprintf("Ok\n");
          }
    }
 
 pushcom()
    {
    extern char wordbuf[];
    extern long mynum;
    long fil;
    long x;
    if(brkword()== -1)
       {
       bprintf("Push what ?\n");
       return;
       }
    nbutt:    x=fobna(wordbuf);
    if(x== -1)
       {
       bprintf("That is not here\n");
       return;
       }
    switch(x)
       {
       case 126:
          bprintf("The tripwire moves and a huge stone crashes down from above!\n");
          broad("\001dYou hear a thud and a squelch in the distance.\n\001");
          loseme();
          crapup("             S   P    L      A         T           !");
       case 162:
          bprintf("A trapdoor opens at your feet and you plumment downwards!\n");
          user.location_id= -140;trapch(user.location_id);
          return;
       case 130:
          if(state(132)==1)
             {
             setstate(132,0);
             bprintf("A secret panel opens in the east wall!\n");
             break;
             }
          bprintf("Nothing happens\n");
          break;
       case 131:
          if(state(134)==1)
             {
             bprintf("Uncovering a hole behind it.\n");
             setstate(134,0);
             }
          break;
       case 138:
          if(state(137)==0)
             {
             bprintf("Ok...\n");
             break;
             }
          else
             {
             bprintf("You hear a gurgling noise and then silence.\n");
             setstate(137,0);
             }
          break;
       case 146:
          ;
       case 147:
          setstate(146,1-state(146));
          bprintf("Ok...\n");
          break;
       case 30:
          setstate(28,1-state(28));
          if(state(28))
             {
             user.send_message("","",-10000,Item(28).location,"\001cThe portcullis falls\n\001");
             user.send_message("","",-10000,Item(29).location,"\001cThe portcullis falls\n\001");
             }
          else
             {
             user.send_message("","",-10000,Item(28).location,"\001cThe portcullis rises\n\001");
             user.send_message("","",-10000,Item(29).location,"\001cThe portcullis rises\n\001");
             }
          break;
       case 149:
          setstate(150,1-state(150));
          if(state(150))
             {
             user.send_message("","",-10000,Item(150).location,"\001cThe drawbridge rises\n\001");
             user.send_message("","",-10000,Item(151).location,"\001cThe drawbridge rises\n\001");
             }
          else
             {
             user.send_message("","",-10000,Item(150).location,"\001cThe drawbridge is lowered\n\001");
             user.send_message("","",-10000,Item(151).location,"\001cThe drawbridge is lowered\n\001");
             }
          break;
       case 24:
          if(state(26)==1)
             {
             setstate(26,0);
             bprintf("A secret door slides quietly open in the south wall!!!\n");
             }
          else
             bprintf("It moves but nothing seems to happen\n");
          return;
       case 49:
          broad("\001dChurch bells ring out around you\n\001");break;
       case 104:if(Player(mynum).helper is None)
	{
		bprintf("You can't shift it alone, maybe you need help\n");
		break;
	}
	/* ELSE RUN INTO DEFAULT */
	goto def2;
       default:;
       	  def2:
          if(Item(x).test_bit(4))
             {
             setstate(x,0);
             oplong(x);
             return;
             }
          if(Item(x).test_bit(5))
             {
             setstate(x,1-state(x));
             oplong(x);
             return;
             }
          bprintf("Nothing happens\n");
          }
    }
 
 cripplecom()
    {
    long a,b;
    extern char globme[];
    extern long mynum;
    b=victim(&a);
    if(b== -1) return;
    user.send_message(Player(a).name,globme,-10101,user.location_id,"");
    }
 
 curecom()
    {
    long a,b;
    extern char globme[];
    extern long mynum;
    b=vichfb(&a);
    if(b== -1) return;
    user.send_message(Player(a).name,globme,-10100,user.location_id,"");
    }
 
 dumbcom()
    {
    long a,b;
    extern long mynum;
    extern char globme[];
    b=victim(&a);
    if(b== -1) return;
    user.send_message(Player(a).name,globme,-10102,user.location_id,"");
    }
 
 forcecom()
    {
    long a,b;
    extern long mynum;
    extern char globme[];
    char z[128];
    b=victim(&a);
    if(b== -1) return;
    getreinput(z);
    user.send_message(Player(a).name,globme,-10103,user.location_id,z);
    }
 
 missilecom()
    {
    long a,b;
    extern long mynum;
    extern char globme[];
    extern long my_lev;
    extern long fighting,in_fight;
    extern long my_sco;
    long ar[8];
    b=vichfb(&a);
    if(b== -1) return;
    sprintf(ar,"%d",my_lev*2);
    user.send_message(Player(a).name,globme,-10106,user.location_id,ar);
    if(Player(a).strength - 2*my_lev<0)    
	{
	bprintf("Your last spell did the trick\n");
	if(not Player(a).is_dead)
	{
	/* Bonus ? */
		if(a<16) my_sco+=(Player(a).level*Player(a).level*100);
		else my_sco+=10*damof(a);
	}
	Player(a).die() /* MARK ALREADY DEAD */
	in_fight=0;
	fighting= -1;
    }
    if(a>15) woundmn(a,2*my_lev);
}
 
 changecom()
    {
    long a,b;
    extern long mynum;
    extern char globme[];
    extern char wordbuf[];
    if(brkword()== -1)
       {
       bprintf("change what (Sex ?) ?\n");
       return;
       }
    if(!!strcmp(wordbuf,"sex"))
       {
       bprintf("I don't know how to change that\n");
       return;
       }
    b=victim(&a);
    if(b== -1) return;
    user.send_message(Player(a).name,globme,-10107,user.location_id,"");
    if(a<16) return;
    Player(a).sex = 1 - Player(a).sex
    }
 
 fireballcom()
    {
    long a,b;
    extern long mynum;
    extern long fighting,in_fight;    
    extern char globme[];
    extern long my_lev;
    extern long my_sco;
    long ar[2];
    b=vichfb(&a);
    if(b== -1) return;
    if(mynum==a)
       {
       bprintf("Seems rather dangerous to me....\n");
       return;
       }
    sprintf(ar,"%d",2*my_lev);
    if(Player(a).strength - (a==fpbns("yeti")?6:2)*my_lev<0)
	{
	bprintf("Your last spell did the trick\n");
	if(not Player(a).is_dead)
	{
	/* Bonus ? */
		if(a<16) my_sco+=(Player(a).level*Player(a).level*100);
		else my_sco+=10*damof(a);
	}
	Player(a).die() /* MARK ALREADY DEAD */
	in_fight=0;
	fighting= -1;
    }    
    user.send_message(Player(a).name,globme,-10109,user.location_id,ar);
    if(a==fpbns("yeti")) {woundmn(a,6*my_lev);return;}
    if(a>15) woundmn(a,2*my_lev);
    }
 
 shockcom()
    {
    long a,b;
    extern long mynum;
    extern char globme[];
    extern long my_lev;
    extern long fighting,in_fight;    
    extern long my_sco;
    long ar[2];
    b=vichfb(&a);
    if(b== -1) return;
    if(a==mynum)
       {
       bprintf("You are supposed to be killing other people not yourself\n");
       return;
       }
       if(Player(a).strength - 2*my_lev<0)
	{
	bprintf("Your last spell did the trick\n");
	if(not Player(a).is_dead)
	{
	/* Bonus ? */
		if(a<16) my_sco+=(Player(a).level*Player(a).level*100);
		else my_sco+=10*damof(a);
	}
	Player(a).die() /* MARK ALREADY DEAD */
	in_fight=0;
	fighting= -1;
    }       
    sprintf(ar,"%d",my_lev*2);
    user.send_message(Player(a).name,globme,-10110,user.location_id,ar);
    if(a>15) woundmn(a,2*my_lev);
    }
 
 starecom()
    {
    extern long mynum;
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(a==mynum)
       {
       bprintf("That is pretty neat if you can do it!\n");
       return;
       }
    sillytp(a,"stares deep into your eyes\n");
    bprintf("You stare at \001p%s\001\n",Player(a).name);
    }
 
 gropecom()
    {
    extern long mynum;
    long a,b;
    extern long isforce;
    if(isforce){bprintf("You can't be forced to do that\n");return;}
    b=vichere(&a);
    if(b== -1) return;
    if(a==mynum)
       {
       bprintf("With a sudden attack of morality the machine edits your persona\n");
       loseme();
       crapup("Bye....... LINE TERMINATED - MORALITY REASONS");
       }
    sillytp(a,"gropes you");
    bprintf("<Well what sort of noise do you want here ?>\n");
    }

 squeezecom()
    {
    extern long mynum;
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(a==mynum)
       {
       bprintf("Ok....\n");
       return;
       }
    if(a== -1) return;
    sillytp(a,"gives you a squeeze\n");
    bprintf("You give them a squeeze\n");
    return;
    }

 kisscom()
    {
    extern long mynum;
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(a==mynum)
       {
       bprintf("Weird!\n");
       return;
       }
    sillytp(a,"kisses you");
    bprintf("Slurp!\n");
    }
 
 cuddlecom()
    {
    extern long mynum;
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(mynum==a)
       {
       bprintf("You aren't that lonely are you ?\n");
       return;
       }
    sillytp(a,"cuddles you");
    }

 hugcom()
    {
    extern long mynum;
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(mynum==a)
       {
       bprintf("Ohhh flowerr!\n");
       return;
       }
    sillytp(a,"hugs you");
    }
 
 slapcom()
    {
    extern long mynum;
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(mynum==a)
       {
       bprintf("You slap yourself\n");
       return;
       }
    sillytp(a,"slaps you");
    }
 
 ticklecom()
    {
    extern long mynum;
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(a==mynum)
       {
       bprintf("You tickle yourself\n");
       return;
       }
    sillytp(a,"tickles you");
    }
 
 /* This one isnt for magic */
 
 vicbase(x)
 long *x;
    {
    long a,b;
    extern char wordbuf[];
    a0:if(brkword()== -1)
       {
       bprintf("Who ?\n");
       return(-1);
       }
    b=openworld();
    if(!strcmp(wordbuf,"at")) goto a0; /* STARE AT etc */
    a=fpbn(wordbuf);
    if(a== -1)
       {
       bprintf("Who ?\n");
       return(-1);
       }
    *x=a;
    return(b);
    }
 
 vichere(x)
long *x;
    {
    long a;
    a=vicbase(x);
    if(a== -1) return(a);
    if(Player(*x).location!=user.location_id)
       {
       bprintf("They are not here\n");
       return(-1);
       }
    return(a);
    }
 
 
 vicf2(x,f1)
long *x;
    {
    extern long mynum;
    long a;
    extern long my_str,my_lev;
    long b,i;
    a=vicbase(x);
    if(a== -1) return(-1);
    if(my_str<10)
       {
       bprintf("You are too weak to cast magic\n");
       return(-1);
       }
    if(my_lev<10) my_str-=2;
i=5;
if(iscarrby(111,mynum)) i++;
if(iscarrby(121,mynum)) i++;
if(iscarrby(163,mynum)) i++;
    if((my_lev<10)&&(randperc()>i*my_lev))
       {
       bprintf("You fumble the magic\n");
       if(f1==1){*x=mynum;bprintf("The spell reflects back\n");}
       else
          {
          return(-1);
          }
       return(a);
       }
 
    else
       {
       if(my_lev<10)bprintf("The spell succeeds!!\n");
       return(a);
       }
    }
 
 vicfb(x)
 long *x;
    {
    return(vicf2(x,0));
    }
 vichfb(x)
 long *x;
    {
    long a;
    a=vicfb(x);
    if(a== -1) return(-1);
    if(Player(*x).location!=user.location_id)
       {
       bprintf("They are not here\n");
       return(-1);
       }
    return(a);
    }
 
 victim(x)
    	long *x;
    {
    return(vicf2(x,1));
    }
 
 sillytp(per,msg)
 char *msg;
    {
    extern char globme[];
    char bk[256];
    if(strncmp(msg,"star",4)==0) 
      sprintf(bk, "%s%s%s%s%s%s%s","\001s",globme,"\001",globme," ",msg,"\n\001");
    else
       sprintf(bk,"%s%s%s%s%s","\001p",globme,"\001 ",msg,"\n");
    user.send_message(Player(per).name,globme,-10111,user.location_id,bk);
    }
 
long ail_dumb=0;
long  ail_crip=0;
long  ail_blind=0;
long  ail_deaf=0;
 
 
 new1rcv(isme,chan,to,from,code,text)
 char *to,*from,*text;
    {
    extern long mynum,my_lev,ail_dumb,ail_crip;
    extern long ail_deaf,ail_blind;
    extern long my_sex;
    extern char globme[];
    switch(code)
       {
       case -10100:
          if(isme==1) {
             bprintf("All your ailments have been cured\n");
             ail_dumb=0;
             ail_crip=0;
             ail_blind=0;ail_deaf=0;
             }
          break;
       case -10101:
          if(isme==1)
             {
             if(my_lev<10)
                {
                bprintf("You have been magically crippled\n");
                ail_crip=1;
                }
 
             else
                bprintf("\001p%s\001 tried to cripple you\n",from);
             }
          break;
       case -10102:
          if(isme==1)
             {
             if(my_lev<10)
                {
                bprintf("You have been struck magically dumb\n");
                ail_dumb=1;
                }
 
             else
                bprintf("\001p%s\001 tried to dumb you\n",from);
             }
          break;
       case -10103:
          if(isme==1)
             {
             if(my_lev<10)
                {
                bprintf("\001p%s\001 has forced you to %s\n",from,text);
                addforce(text);
                }
 
             else
                bprintf("\001p%s\001 tried to force you to %s\n",from,text);
             }
          else
          break;
       case -10104:
          if(isme!=1)bprintf("\001p%s\001 shouts '%s'\n",from,text);
          break;
       case -10105:
          if(isme==1)
             {
             if(my_lev<10)
                {
                bprintf("You have been struck magically blind\n");
                ail_blind=1;
                }
 
             else
                bprintf("\001p%s\001 tried to blind you\n",from);
             }
          break;
       case -10106:
          if(iam(from))break;
          if(user.location_id==chan)
             {
             bprintf("Bolts of fire leap from the fingers of \001p%s\001\n",from);
             if(isme==1)
                {
                bprintf("You are struck!\n");
                wounded(numarg(text));
                }
 
             else
                bprintf("\001p%s\001 is struck\n",to);
             }
          break;
       case -10107:
          if(isme==1)
             {
             bprintf("Your sex has been magically changed!\n");
             my_sex=1-my_sex;
             bprintf("You are now ");
             if(my_sex)bprintf("Female\n");
             else
                bprintf("Male\n");
             calibme();
             }
          break;
       case -10109:
          if(iam(from)) break;
          if(user.location_id==chan)
             {
             bprintf("\001p%s\001 casts a fireball\n",from);
             if(isme==1)
                {
                bprintf("You are struck!\n");
                wounded(numarg(text));
                }
 
             else
                bprintf("\001p%s\001 is struck\n",to);
             }
          break;
       case -10110:
          if(iam(from)) break;
          if(isme==1)
             {
             bprintf("\001p%s\001 touches you giving you a sudden electric shock!\n",from);
             wounded(numarg(text));
             }
          break;
       case -10111:
          if(isme==1)bprintf("%s\n",text);
          break;
       case -10113:
          if(my_lev>9)bprintf("%s",text);
          break;
       case -10120:
          if(isme==1)
             {
             if(my_lev>9)
                {
                bprintf("\001p%s\001 tried to deafen you\n",from);
                break;
                }
             bprintf("You have been magically deafened\n");
             ail_deaf=1;
             break;
             }
          }
    }
 
 destroy(ob)
    {
    Item(ob).set_bit(0);
    }
 
 tscale()
    {
    long a,b;
    a=0;
    b=0;
    while(b<16)
       {
       if(Player(b).exists) a++;
       b++;
       }
    switch(a)
       {
       case 1:
          return(2);
       case 2:
          return(3);
       case 3:
          return(3);
       case 4:
          return(4);
       case 5:
          return(4);
       case 6:
          return(5);
       case 7:
          return(6);
       default:
          return(7);
          }
    }
 
 chkdumb()
    {
    extern long ail_dumb;
    if(!ail_dumb) return(0);
    bprintf("You are dumb...\n");
    return(1);
    }
 
 chkcrip()
    {
    extern long ail_crip;
    if(!ail_crip) return(0);
    bprintf("You are crippled\n");
    return(1);
    }

 chkblind()
    {
    extern long ail_blind;
    if(!ail_blind) return(0);
    bprintf("You are blind, you cannot see\n");
    return(1);
    }
 
 chkdeaf()
    {
    extern long ail_deaf;
    if(!ail_deaf) return(0);
    return(1);
    }
 
 wounded(n)
    {
    extern long my_str,my_lev;
    extern long me_cal;
    extern long zapped;
    extern char globme[];
    char ms[128];
    if(my_lev>9) return;
    my_str-=n;
    me_cal=1;
    if(my_str>=0) return;
    closeworld();
    syslog("%s slain magically",globme);
    delpers(globme);
    zapped=1;
    openworld();
    dumpitems();
    loseme();
    sprintf(ms,"%s has just died\n",globme);
    user.send_message(globme,globme,-10000,user.location_id,ms);
    sprintf(ms,"[ %s has just died ]\n",globme);
    user.send_message(globme,globme,-10113,user.location_id,ms);
    crapup("Oh dear you just died\n");
    }
 
 woundmn(mon,am)
    {
    extern long mynum;
    extern char globme[];
    long a;
    long b;
    char ms[128];
    a=Player(mon).strength - am;
    Player(mon).strength = a;
 
    if(a>=0){mhitplayer(mon,mynum);}
 
    else
       {
       dumpstuff(mon,Player(mon).location);
       sprintf(ms,"%s has just died\n",Player(mon).name);
       user.send_message(" "," ",-10000,Player(mon).location,ms);
       sprintf(ms,"[ %s has just died ]\n",Player(mon).name);
       Player(mon).remove()
       user.send_message(globme,globme,-10113,Player(mon).location,ms);
       }
    }
 
 
 mhitplayer(mon,mn)
    {
    extern long my_lev,mynum;
    long a,b,x[4];
    extern char globme[];
    if(Player(mon).location !=user.location_id) return;
    if((mon<0)||(mon>47)) return;
    a=randperc();
    b=3*(15-my_lev)+20;
if((iswornby(89,mynum))||(iswornby(113,mynum))||(iswornby(114,mynum)))
       b-=10;
    if(a<b)
       {
       x[0]=mon;
       x[1]=randperc()%damof(mon);
       x[2]= -1;
       user.send_message(globme,Player(mon).name,-10021,Player(mon).location,(char *)x);
       }
 
    else
       {
 
       x[0]=mon;
       x[2]= -1;
       x[1]= -1;
       user.send_message(globme,Player(mon).name,-10021,Player(mon).location,x) ;
       }
    }
 
 resetplayers()
    {
    extern PLAYER pinit[];
    long a,b,c;
    a=16;
    c=0;
    while(a<35)
       {
       strcpy(Player(a).name,pinit[c].p_name);
       Player(a).location = pinit[c].p_loc
       Player(a).strength = pinit[c].p_str
       setpsex(a,pinit[c].p_sex);
       Player(a).weapon = None
       Player(a).visible = 0
       Player(a).level = pinit[c].p_lev);
       a++;c++;
       }
    while(a<48)
       {
       strcpy(Player(a).name,"");
       a++;
       }
    }
 
PLAYER pinit[48]=
    { "The Wraith",-1077,60,0,-2,"Shazareth",-1080,99,0,-30,"Bomber",-308,50,0,-10,
    "Owin",-311,50,0,-11,"Glowin",-318,50,0,-12,
    "Smythe",-320,50,0,-13
    ,"Dio",-332,50,0,-14
    ,"The Dragon",-326,500,0,-2,"The Zombie",-639,20,0,-2
    ,"The Golem",-1056,90,0,-2,"The Haggis",-341,50,0,-2,"The Piper"
    ,-630,50,0,-2,"The Rat",-1064,20,0,-2
    ,"The Ghoul",-129,40,0,-2,"The Figure",-130,90,0,-2,
    "The Ogre",-144,40,0,-2,"Riatha",-165,50,0,-31,
    "The Yeti",-173,80,0,-2,"The Guardian",-197,50,0,-2
    ,"Prave",-201,60,0,-400,"Wraith",-350,60,0,-2
    ,"Bath",-1,70,0,-401,"Ronnie",-809,40,0,-402,"The Mary",-1,50,0,-403,
    "The Cookie",-126,70,0,-404,"MSDOS",-1,50,0,-405,
    "The Devil",-1,70,0,-2,"The Copper"
    ,-1,40,0,-2
    };
 
 
 
 wearcom()
    {
    long a,b;
    extern long mynum;
    b=ohereandget(&a);
    if(b== -1) return(-1);
    if(!iscarrby(a,mynum))
       {
       bprintf("You are not carrying this\n");
       return;
       }
    if(iswornby(a,mynum))
       {
       bprintf("You are wearing this\n");
       return;
       }
    if(((iswornby(89,mynum))||(iswornby(113,mynum))||(iswornby(114,mynum)))&&
         ((a==89)||(a==113)||(a==114)))
         {
         	bprintf("You can't use TWO shields at once...\n");
         	return;
        }
    if(!canwear(a))
       {
       bprintf("Is this a new fashion ?\n");
       return;
       }
    setcarrf(a,2);
    bprintf("OK\n");
    }
 
 removecom()
    {
    long a,b;
    extern long mynum;
    b=ohereandget(&a);
    if(b== -1) return;
    if(!iswornby(a,mynum))
       {
       bprintf("You are not wearing this\n");
       }
    setcarrf(a,1);
    }
 
 setcarrf(o,n)
    {
    extern long objinfo[];
    objinfo[4*o+3]=n;
    }
 
 iswornby(item,chr)
    {
    if(!iscarrby(item,chr)) return(0);
    if(Item(item).carry_flag!=2) return(0);
    return(1);
    }

 addforce(x)
 char *x;
    {
    extern char acfor[];
    extern long forf;
    if(forf==1)bprintf("The compulsion to %s is overridden\n",acfor);
    forf=1;
    strcpy(acfor,x);
    }
 
long forf=0;
char acfor[128];
 
 forchk()
    {
    extern long forf;
    extern char acfor[];
    extern long isforce;
    isforce=1;
    if(forf==1) gamecom(acfor);
    isforce=0;
    forf=0;
    }
 
long isforce=0;
 damof(n)
    {
    switch(n)
       {
       case 20:
case 18:;
case 19:;
case 21:;
case 22:;
          return(6);
       case 23:
          return(32);
       case 24:
          return(8);
       case 28:
          return(6);
case 30:return(20);
case 31:return(14);
case 32:return(15);
case 33:return(10);
       default:
          return(10);
          }
    }
 canwear(a)
    {
    switch(a)
       {
       default:
          if(Item(a).test_bit(8)) return(1);
          return(0);
          }
    }
 iam(x)
 char *x;
    {
    char a[64],b[64];
    extern char globme[];
    strcpy(a,x);
    strcpy(b,globme);
    lowercase(a);
    lowercase(b);
    if(!strcmp(a,b)) return(1);
    if(strncmp(b,"the ",4)==0)
       {
       if(!strcmp(a,b+4)) return(1);
       }
    return(0);
    }
 deafcom()
    {
    long a,b;
    extern long mynum;
    extern char globme[64];
    b=victim(&a);
    if(b== -1) return;
    user.send_message(Player(a).name,globme,-10120,user.location_id,"");
    }
 
blindcom()
    {
    long a,b;
    extern long mynum;
    extern char globme[64];
    b=victim(&a);
    if(b== -1) return;
    user.send_message(Player(a).name,globme,-10105,user.location_id,"");
    }

teletrap(newch)
long newch;
{
       char block[200];
       sprintf(block,"%s%s%s%s%s","\001s",globme,"\001",globme," has left.\n\001");
       user.send_message(globme,globme,-10000,user.location_id,block);
       user.location_id=newch;
       sprintf(block,"%s%s%s%s%s","\001s",globme,"\001",globme," has arrived.\n\001");
       user.send_message(globme,globme,-10000,newch,block);
       trapch(user.location_id);
}

on_flee_event()
{
	extern long  numobs;
	extern long mynum;
	long ct=0;
	while(ct<numobs)
	{
		if((iscarrby(ct,mynum))&&(!iswornby(ct,mynum)))
		{
			Item(ct).set_location(Player(mynum).location, 0);
		}
		ct++;
	}
}
"""