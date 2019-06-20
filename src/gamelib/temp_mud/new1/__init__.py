"""
Extensions section 1
"""
from ..magic import randperc
from ..newuaf import NewUaf
from ..parse.messages import Message
from ..support import Item, Player


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