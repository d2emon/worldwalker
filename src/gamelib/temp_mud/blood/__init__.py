class Blood:
    fighting = None
    in_fight = 0

    @classmethod
    def stop_fight(cls):
        cls.in_fight = 0
        cls.fighting = None

    @classmethod
    def get_enemy(cls):
        return Player(cls.fighting)

    # Parse
    @classmethod
    def check_fight(cls):
        if cls.fighting is not None and cls.get_enemy().exists:
            cls.stop_fight()

        if cls.in_fight:
            cls.in_fight -= 1


"""
#include <stdio.h>
#include "files.h"
#include "System.h"



long in_fight=0;
long  fighting= -1;



int dambyitem(it)
long it;
    {
    switch(it)
       {
case -1:return(4);
default:if(!Item(it).test_bit(15))return(-1);
else return(Item(it).get_byte(0));
          }

    }

long wpnheld= -1;

void weapcom()
    {
    long a,b;
    if(brkword()== -1)
       {
       bprintf("Which weapon do you wish to select though\n");
       return;
       }
    a = Item.find(
	    wordbuf,
	    owner=parser.use,
	    destroyed=parser.user.is_wizard,
	)
    if(a== -1)
       {
       bprintf("Whats one of those ?\n");
       return;
       }
    b=dambyitem(a);
    if(b<0)
       {
       bprintf("Thats not a weapon\n");
       wpnheld= -1;
       return;
       }
    wpnheld=a;
        yield from user.update()
    bprintf("OK...\n");
    }

void hitplayer(victim,wpn)
 long victim,wpn;
    {
    long a,b,c,d;
    extern long wpnheld;
    long z;
    long x[4];
    long cth,ddn,res;
    if(not Player(victim).exists) return;
    /* Chance to hit stuff */
    if((!wpn.is_carried_by(user))&&(wpn!= -1))
       {
       bprintf("You belatedly realise you dont have the %s,\nand are forced to use your hands instead..\n",Item(wpn).name);
       if(wpnheld==wpn) wpnheld= -1;
       wpn= -1;
       }
    wpnheld=wpn;
    if((wpn==32)&&(Item(16)..is_carried_by(victim)))
    {
        bprintf("The runesword flashes back away from its target, growling in anger!\n");
        return;
    }
    if(dambyitem(wpn)<0)
       {
       bprintf("Thats no good as a weapon\n");
       wpnheld= -1;
       return;
       }
	if(in_fight)
	{
		bprintf("You are already fighting!\n");
		return;
	}
	fighting=victim;
	in_fight=300;
	res=randperc();
	cth=40+3*user.level;
	if((Item(89).is_worn_by(victim))||Item(113).is_worn_by(victim)||Item(114).is_worn_by(victim))
        cth-=10;
	if(cth<0) cth=0;
	if(cth>res)
        {
	       bprintf("You hit \001p%s\001 ",Player(victim).name);
 	       if(wpn!= -1)bprintf("with the %s",Item(wpn).name);
	       bprintf("\n");
	       ddn=randperc()%(dambyitem(wpn));
	       x[0]=user;
	       x[1]=ddn;
	       x[2]=wpn;
	       if(Player(victim).strength < ddn)
		{
			bprintf("Your last blow did the trick\n");
			if(not Player(victim).is_dead)
			{
/* Bonus ? */
				if(victim<16)
				    user.score+=(Player(victim).level*Player(victim).level*100);
				else
				    user.score += victim.value
			}
			Player(victim).die(); /* MARK ALREADY DEAD */
			in_fight=0;
			fighting= -1;
		}
       if(victim<16) user.send_message(Player(victim).name,globme,-10021,user.location_id,(char *)x);
       else
          	{
          	victim.get_damage(parser.user, ddn)
          	}
       user.score+=ddn*2;
        yield from user.update()
       return;
       }
    else
       {
	       bprintf("You missed \001p%s\001\n",Player(victim).name);
	       x[0]=user;
	       x[1]= -1;
	       x[2]=wpn;
	       if(victim<16) user.send_message(Player(victim).name,globme,-10021,user.location_id,(char *)x);
     		else
          	victim.get_damage(parser.user, 0)
       }
    }

 killcom()
    {
    long vic,a;
    long x;
    if(brkword()== -1)
       {
       bprintf("Kill who\n");
       return;
       }
    if(!strcmp(wordbuf,"door"))
	{
		bprintf("Who do you think you are , Moog ?\n");
		return;
	}
	item = Item.find(
	    wordbuf,
	    available=True,
	    destroyed=parser.user.is_wizard,
	)
	if item is not None:
       {
	       breakitem(item);
	       return;
       }
    if((a=parser.user.find(wordbuf))== -1)
       {
	       bprintf("You can't do that\n");
	       return;
       }
    if(a==user)
       {
	       bprintf("Come on, it will look better tomorrow...\n");
	       return;
       }
    if(Player(a).location!=user.location_id)
       {
	       bprintf("They aren't here\n");
	       return;
       }
    xwisc:if(brkword()== -1)
       {
	       hitplayer(a,wpnheld);
	       return;
       }
    if(!strcmp(wordbuf,"with"))
       {
	       if(brkword()== -1)
	          {
		          bprintf("with what ?\n");
		          return;
	          }
	       }
	    else
	       goto xwisc;
        x = Item.find(
            wordbuf,
            owner=parser.user,
            destroyed=parser.user.is_wizard,
        )
	    if(x== -1)
	       {
		       bprintf("with what ?\n");
		       return;
	       }
    hitplayer(a,x);
    }


void  bloodrcv(array,isme)
 long *array;
    {
    long x;
    char ms[128];
    if(!isme) return; /* for mo */
    if(array[0]<0) return;
    nlod:if(not Player(array[0]).exists) return;
    fighting=array[0];
    in_fight=300;
    if(array[1]== -1)
       {
       bprintf("\001p%s\001 attacks you",Player(array[0]).name);
       if(array[2]!= -1)bprintf(" with the %s",Item(array[2]).name);
       bprintf("\n");
       }
    else
       {
       bprintf("You are wounded by \001p%s\001",Player(array[0]).name);
       if(array[2]>-1)bprintf(" with the %s", Item(array[2]).name);
       bprintf("\n");
       if(not user.is_wizard){user.strength-=array[1];
    if(array[0]==16) {
    	    user.score-=100*array[1];
	    bprintf("You feel weaker, as the wraiths icy touch seems to drain your very life force\n");
	    if(user.score<0) user.strength= -1;
	    }
    }
    if(user.is_dead)
    {
          syslog("%s slain by %s",globme,Player(array[0]).name);
          parser.user.dump_items()
          user.loose()
          World.save()
          user.remove()
          World.load()
          sprintf(ms,"\001p%s\001 has just died.\n",globme);
          user.send_message(globme,globme,-10000,user.location_id,ms);
          sprintf(ms,"[ \001p%s\001 has been slain by \001p%s\001 ]\n",globme,Player(array[0]).name);
          user.send_message(globme,globme,-10113,user.location_id,ms);
          crapup("Oh dear... you seem to be slightly dead\n");
          }
       me_cal=1; /* Queue an update when ready */
       }
    }


void  breakitem(x)
    {
    switch(x)
       {
	case 171:sys_reset();break;
	case -1:
          bprintf("What is that ?\n");break;
       default:
          bprintf("You can't do that\n");
          }
    }
"""
