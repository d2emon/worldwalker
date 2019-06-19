"""
Extensions section 1
"""
from ..magic import randperc
from ..newuaf import NewUaf
from ..parse.messages import Message
from ..support import Item, Player
from ..tk import Tk
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


MOBILES = [
    # 0-15
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


def woundmn(enemy, damage):
    new_strength = enemy.strength - damage
    enemy.strength = new_strength

    if new_strength >= 0:
        return mhitplayer(enemy)

    enemy.dump_items()
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
    to_hit = 3 * (15 - NewUaf.level) + 20
    if Item(89).is_worn_by(user) or Item(113).is_worn_by(user) or Item(114).is_worn_by(user):
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
    Message(
        Tk,
        Tk,
        MSG_GLOBAL,
        new_channel,
        "\001s{name}\001{name} has arrived.\n\001".format(name=Tk.globme),
    ).send()
    user.go_to_location(new_channel)


def on_flee_event():
    for item_id in range(ObjSys.numobs):
        item = Item(item_id)
        if item.is_carried_by(user) and not item.is_worn_by(user):
            item.set_location(user.location, 0)


"""
 wounded(n)
    {
    extern long me_cal;
    extern long zapped;
    extern char globme[];
    char ms[128];
    if(user.is_wizard) return;
    user.strength -= n;
    me_cal=1;
    if(not user.is_dead) return;
          World.save()
    syslog("%s slain magically",globme);
    user.remove()
    zapped=1;
          World.load()
    parser.user.dump_items()
    user.loose();
    sprintf(ms,"%s has just died\n",globme);
    user.send_message(globme,globme,-10000,user.location_id,ms);
    sprintf(ms,"[ %s has just died ]\n",globme);
    user.send_message(globme,globme,-10113,user.location_id,ms);
    crapup("Oh dear you just died\n");
    }
 
 woundmn(mon,am)
    {
    extern char globme[];
    long a;
    long b;
    char ms[128];
    a=Player(mon).strength - am;
    Player(mon).strength = a;
 
    if(a>=0){mhitplayer(mon,user);}
 
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
    long a,b,x[4];
    extern char globme[];
    if(Player(mon).location !=user.location_id) return;
    if((mon<0)||(mon>47)) return;
    a=randperc();
    b=3*(15 - user.level) + 20;
if((iswornby(89,user))||(iswornby(113,user))||(iswornby(114,user)))
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
    b=ohereandget(&a);
    if(b== -1) return(-1);
    if(!a.is_carried_by(user))
       {
       bprintf("You are not carrying this\n");
       return;
       }
    if(iswornby(a,user))
       {
       bprintf("You are wearing this\n");
       return;
       }
    if(((iswornby(89,user))||(iswornby(113,user))||(iswornby(114,user)))&&
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
    b=ohereandget(&a);
    if(b== -1) return;
    if(!iswornby(a,user))
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
    if(!item.is_carried_by(chr)) return(0);
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
    extern char globme[64];
    b=victim(&a);
    if(b== -1) return;
    user.send_message(Player(a).name,globme,-10120,user.location_id,"");
    }
 
blindcom()
    {
    long a,b;
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
       sprintf(block,"%s%s%s%s%s","\001s",globme,"\001",globme," has arrived.\n\001");
       user.send_message(globme,globme,-10000,newch,block);
       user.location = newch
}

on_flee_event()
{
	extern long  numobs;
	long ct=0;
	while(ct<numobs)
	{
		if((ct.is_carried_by(user))&&(!iswornby(ct,user)))
		{
			Item(ct).set_location(user.location, 0);
		}
		ct++;
	}
}
"""