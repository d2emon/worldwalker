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


def tscale():
    players = len(list(filter(lambda player: len(player.name) > 0, [Player(b) for b in range(16)])))
    return SCALES.get(players, 7)


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
 starecom()
    {
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(a==user)
       {
       bprintf("That is pretty neat if you can do it!\n");
       return;
       }
    sillytp(a,"stares deep into your eyes\n");
    bprintf("You stare at \001p%s\001\n",Player(a).name);
    }
 
 gropecom()
    {
    long a,b;
    extern long isforce;
    if(isforce){bprintf("You can't be forced to do that\n");return;}
    b=vichere(&a);
    if(b== -1) return;
    if(a==user)
       {
       bprintf("With a sudden attack of morality the machine edits your persona\n");
       raise LooseError("Bye....... LINE TERMINATED - MORALITY REASONS");
       }
    sillytp(a,"gropes you");
    bprintf("<Well what sort of noise do you want here ?>\n");
    }

 squeezecom()
    {
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(a==user)
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
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(a==user)
       {
       bprintf("Weird!\n");
       return;
       }
    sillytp(a,"kisses you");
    bprintf("Slurp!\n");
    }
 
 cuddlecom()
    {
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(user==a)
       {
       bprintf("You aren't that lonely are you ?\n");
       return;
       }
    sillytp(a,"cuddles you");
    }

 hugcom()
    {
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(user==a)
       {
       bprintf("Ohhh flowerr!\n");
       return;
       }
    sillytp(a,"hugs you");
    }
 
 slapcom()
    {
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(user==a)
       {
       bprintf("You slap yourself\n");
       return;
       }
    sillytp(a,"slaps you");
    }
 
 ticklecom()
    {
    long a,b;
    b=vichere(&a);
    if(b== -1) return;
    if(a==user)
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
          b = World.load()
    if(!strcmp(wordbuf,"at")) goto a0; /* STARE AT etc */
    a=parser.user.find(wordbuf);
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
    long a;
    long b,i;
    a=vicbase(x);
    if(a== -1) return(-1);
    if(user.strength<10)
       {
       bprintf("You are too weak to cast magic\n");
       return(-1);
       }
    if(not user.is_wizard) user.strength-=2;
i=5;
if(Item(111).is_carried_by(user)) i++;
if(Item(121).is_carried_by(user)) i++;
if(Item(163).is_carried_by(user)) i++;
    if((not user.is_wizard)&&(randperc()>i * user.level))
       {
       bprintf("You fumble the magic\n");
       if(f1==1){*x=user;bprintf("The spell reflects back\n");}
       else
          {
          return(-1);
          }
       return(a);
       }
 
    else
       {
       if(not user.is_wizard)bprintf("The spell succeeds!!\n");
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
    extern long ail_dumb,ail_crip;
    extern long ail_deaf,ail_blind;
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
             if(not user.is_wizard)
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
             if(not user.is_wizard)
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
             if(not user.is_wizard)
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
             if(not user.is_wizard)
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
             user.sex = 1 - user.sex
             bprintf("You are now ");
             if(user.sex)bprintf("Female\n");
             else
                bprintf("Male\n");
        yield from user.update()
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
          if(user.is_wizard)bprintf("%s",text);
          break;
       case -10120:
          if(isme==1)
             {
             if(user.is_wizard)
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