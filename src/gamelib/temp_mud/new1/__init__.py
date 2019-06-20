"""
Extensions section 1
"""
from ..magic import randperc
from ..newuaf import NewUaf
from ..parse.messages import Message
from ..support import Item, Player


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