objinfo = []
"""
/*

 Object structure

 Name,
 Long Text 1
 Long Text 2
 Long Text 3
 Long Text 4
 statusmax
 Value
 flags (0=Normal 1+flannel)

 */

#define NOBS 194
#define OBMUL 8
#include <stdio.h>

long numobs=NOBS;
extern FILE *openlock();
extern FILE *openworld();

long objinfo[NOBS*4];


 inventory()
    {
    extern long mynum;
   bprintf("You are carrying\n");
    lobjsat(mynum);
    }

 /*
 Objinfo

 Loc
 Status
 Stamina
 Flag 1=carr 0=here
 */

lobjsat(loc)
{
aobjsat(loc,1);
}


aobjsat(loc,mode)  /* Carried Loc ! */
    {
    long a,b,c,d,e,f;
    char x[6],y[6];
    extern long debug_mode;
    b=0;
    c=0;
    d=0;
    e=0;
    f=0;
    while(c<NOBS)
       {
       if(((iscarrby(c,loc))&&(mode==1))||
((iscontin(c,loc))&&(mode==3)))
          {
          e=1;
              f+=1+strlen(Item.load(c).name);
if(debug_mode){ f+=5;sprintf(x,"%d",c);sprintf(y,"{%-3s}",x);}
if(Item.load(c).is_destroyed) f+=2;
if(iswornby(c,loc)) f+=strlen("<worn> ");
          if(f>79)
             {
             f=0;
            bprintf("\n");
             }
if(Item.load(c).is_destroyed) bprintf("(");
         bprintf("%s",Item.load(c).name);
         if(debug_mode) bprintf(y);
if(iswornby(c,loc)) bprintf(" <worn>");
if(Item.load(c).is_destroyed) bprintf(")");
bprintf(" ");
          f++;
          }
       d+=4;
       c++;
       }
    if(!e)bprintf("Nothing");
   bprintf("\n");
    }


iscontin(o1,o2)
{
extern long my_lev;
if(not Item.load(o1).is_in_item) return(0)
;
if(Item.load(o1).location_id!=o2) return(0);
if((my_lev<10)&&(Item.load(o1).is_destroyed))return(0);
return(1);
}

fobnsys(nam,ctrl,ct_inf)
char *nam;
long ctrl,ct_inf;
{
    extern char wd_it[];
    extern long mynum;
    long a;
    long l1[32],l2[32];
    extern char wordbuf[];
    strcpy(l1,nam);lowercase(l1);
    a=0;
if(!strcmp(l1,"red")) {brkword();return(4);}
if(!strcmp(l1,"blue")) {brkword();return(5);}
if(!strcmp(l1,"green")) {brkword();return(6);}
    while(a<NOBS)
       {
       strcpy(l2,Item.load(a).name);lowercase(l2);
       if(!strcmp(l1,l2))
          {
	  strcpy(wd_it,nam);
          switch(ctrl)
             {
             case 0:
                return(a);
             case 1:/* Patch for shields */
                if((a==112)&&(iscarrby(113,mynum))) return(113);
                if((a==112)&&(iscarrby(114,mynum))) return(114);
                if(Item.load(a).available_for(mynum)) return(a);
                break;
             case 2:
                if(iscarrby(a,mynum)) return(a);
                break;
             case 3:
                if(iscarrby(a,ct_inf)) return(a);
                break
                ;
             case 4:
                if(ishere(a)) return(a);
                break;
             case 5:
                if(iscontin(a,ct_inf)) return(a);
                break;
             default:
                return(a);
                }
          }
       a++;
       }
    return(-1);
    }

 fobn(word)
 char *word;
    {
long x;
x=fobna(word);
if(x!=-1) return(x);
    return(fobnsys(word,0,0));
    }

 fobna(word)
 char *word;
    {
    return(fobnsys(word,1,0));
    }

 fobnin(word,ct)
 char *word;
 long ct;
 {
 	return(fobnsys(word,5,ct));	
 }

 fobnc(word)
 char *word;
    {
    return(fobnsys(word,2,0));
    }

 fobncb(word,by)
 char *word;
    {
    return(fobnsys(word,3,by));
    }

 fobnh(word)
 char *word;
    {
    return(fobnsys(word,4,0));
    }
    
 getobj()
    {
    extern long mynum;
    extern char globme[];
    extern long curch;
    extern char wordbuf[];
    long a,b;
    long i;
    long des_inf= -1;
    extern long stp;
    char bf[256];
    if(brkword()==-1)
       {
      bprintf("Get what ?\n");
       return;
       }
    a=fobnh(wordbuf);
    /* Hold */
    i=stp;
    strcpy(bf,wordbuf);
    if((brkword()!=-1)&&((strcmp(wordbuf,"from")==0)||(strcmp(wordbuf,"out")==0)))
    {
    	if(brkword()==-1)
    	{
    		bprintf("From what ?\n");
    		return;
    	}
    	des_inf=fobna(wordbuf);
    	if(des_inf==-1)
    	{
    		bprintf("You can't take things from that - it's not here\n");
    		return;
    	}
    	a=fobnin(bf,des_inf);
    }
    stp=i;
    if(a==-1)
       {
      bprintf("That is not here.\n");
       return;
       }
if((a==112)&&(des_inf==-1))
{
if(Item.load(113).is_destroyed) a=113;
else if(Item.load(114).is_destroyed) a=114;
if((a==113)||(a==114)) Item.load(a).create()
else bprintf("The shields are all to firmly secured to the walls\n");
}
    if(Item.load(a).is_movable)
       {
      bprintf("You can't take that!\n");
       return;
       }
if(dragget()) return;
    if(!cancarry(mynum))
       {
      bprintf("You can't carry any more\n");
       return;
}
if((a==32)&&(state(a)==1)&&(next(PlayerCharacter.load(mynum).helpers, None) is None))
{
	bprintf("Its too well embedded to shift alone.\n");
	return;
}
    Item.load(a).set_location_held(mynum);
    sprintf(bf,"\001D%s\001\001c takes the %s\n\001",globme,Item.load(a).name);
   bprintf("Ok...\n");
    sendsys(globme,globme,-10000,curch,bf);
if(Item.load(a).get_flag(Item.FLAG_12)) setstate(a,0);
if(curch==-1081) 
{
	setstate(20,1);
	bprintf("The door clicks shut....\n");
}
    }

 ishere(item)
    {
    extern long curch;
    long a;
extern long my_lev;
    if((my_lev<10)&&(Item.load(item).is_destroyed))return(0);
    if(Item.load(item).is_held) return(0);
    if(Item.load(item).location_id!=curch) return(0);
    return(1);
    }

 iscarrby(item,user)
    {
    extern long curch;
extern long my_lev;
    if((my_lev<10)&&(Item.load(item).is_destroyed))return(0);
    if((not Item.load(item).is_held)&&(not Item.load(item).is_worn)) return(0);
    if(Item.load(item).location_id!=user) return(0);
    return(1);
    }

 dropitem()
    {
    extern long mynum,curch;
    extern char wordbuf[],globme[];
    extern long my_sco;
    long a,b,bf[32];
    extern long my_lev;
    if(brkword()==-1)
       {
      bprintf("Drop what ?\n");
       return;
       }
    a=fobnc(wordbuf);
    if(a==-1)
       {
      bprintf("You are not carrying that.\n");
       return;
       }

if((my_lev<10)&&(a==32))
{
bprintf("You can't let go of it!\n");
return;
}
    Item.load(a).set_location_channel(curch);
   bprintf("OK..\n");
    sprintf(bf,"\001D%s\001\001c drops the %s.\n\n\001",globme,wordbuf);
    sendsys(globme,globme,-10000,curch,bf);
    if((curch!=-183)&&(curch!=-5))return;
   sprintf(bf,"The %s disappears into the bottomless pit.\n",wordbuf);
   bprintf("It disappears down into the bottomless pit.....\n");
    sendsys(globme,globme,-10000,curch,bf);
    my_sco+=(tscale()*Item.load(a).base_value)/5;
    calibme();
Item.load(a).set_location_channel(-6);
    }
 lisobs()
    {
    lojal2(1);
    showwthr();
    lojal2(0);
    }

 lojal2(n)
    {
    extern char wd_it[];
    long a;
    a=0;
    while(a<NOBS)
       {
       if((ishere(a))&&(Item.load(a).is_movable != n))
          {
              if(state(a)>3) continue;
              if(!!strlen(Item.load(a).get_description(state(a)))) /*OLONGT NOTE TO BE ADDED */
		{
			if(Item.load(a).is_destroyed) bprintf("--");
 
				oplong(a);
		          strcpy(wd_it,Item.load(a).name);
		}
          }
       a++;
       }
    }
 dumpitems()
    {
    extern long mynum;
    extern long curch;
    dumpstuff(mynum,curch);
    }

 dumpstuff(n,loc)
    {
    long b;
    b=0;
    while(b<NOBS)
       {
       if(iscarrby(b,n))

          {
          Item.load(b).set_location_channel(loc);
          }
       b++;
       }
    }

long ublock[16*49];


 whocom()
    {
    long a;
    extern long my_lev;
    long bas;
    a=0;
    bas=16;
    if(my_lev>9)
       {
      bprintf("Players\n");
       bas=48;
       }
    while(a<bas)
       {
       if(a==16)bprintf("----------\nMobiles\n");
       if(!PlayerCharacter.load(a).exists) goto npas;
       dispuser(a);
       npas:a++;
       }
   bprintf("\n");
    }

 dispuser(ubase)
    {
extern long my_lev;
    if(PlayerCharacter.load(ubase).is_dead) return; /* On  Non game mode */
    if(not PlayerCharacter.load(ubase).visible_for(my_lev)) return;
if(PlayerCharacter.load(ubase).visible) bprintf("(");
   bprintf("%s ",PlayerCharacter.load(ubase).name);
    disl4(PlayerCharacter.load(ubase).level,PlayerCharacter.load(ubase).sex);
if(PlayerCharacter.load(ubase).visible) bprintf(")");
if(PlayerCharacter.load(ubase).is_absent) bprintf(" [Absent From Reality]");
bprintf("\n");
    }

 disle3(n,s)
    {
    disl4(n,s);
   bprintf("\n");
    }
 disl4(n,s)
    {
    extern long hasfarted;
    switch(n)
       {
       case 1:
         bprintf("The Novice");
          break;
       case 2:
          if(!s)bprintf("The Adventurer");
          else
            bprintf("The Adventuress");
          break;
       case 3:
         bprintf("The Hero");
          if(s)bprintf("ine");
          break;
       case 4:
         bprintf("The Champion");
          break;
       case 5:
          if(!s)bprintf("The Conjurer");
          else
            bprintf("The Conjuress");
          break;
       case 6:
         bprintf("The Magician");
          break;
       case 7:
          if(s)bprintf("The Enchantress");
          else
            bprintf("The Enchanter");
          break;
       case 8:
          if(s)bprintf("The Sorceress");
          else
            bprintf("The Sorceror");
          break;
case 9:bprintf("The Warlock");
break;
       case 10:
          if(s)bprintf("The Apprentice Witch");
          else
            bprintf("The Apprentice Wizard");
          break;
case 11:bprintf("The 370");
break;
case 12:bprintf("The Hilbert-Space");
break;
case 14:bprintf("The Completely Normal Naughty Spud");
break;
case 15:bprintf("The Wimbledon Weirdo");
break;
case 16:bprintf("The DangerMouse");
break;
case 17:bprintf("The Charred Wi");
if(s) bprintf("tch");
else bprintf("zard");
break;
case 18:bprintf("The Cuddly Toy");
break;
case 19:if(!hasfarted) bprintf("Of The Opera");
else bprintf("Raspberry Blower Of Old London Town");
break;
case 20:bprintf("The 50Hz E.R.C.S");
break;
case 21:bprintf("who couldn't decide what to call himself");
break;
case 22:bprintf("The Summoner");
break;
case 10000:
bprintf("The 159 IQ Mega-Creator");
break;
case 10033:
case 10001:bprintf("The Arch-Wi");
if(s)bprintf("tch");
else bprintf("zard");
break;
case 10002:bprintf("The Wet Kipper");
break;
case 10003:bprintf("The Thingummy");
break;
case 68000:
bprintf("The Wanderer");
break;
case -2:
bprintf("\010");
break;
case -11:bprintf("The Broke Dwarf");break;
case -12:bprintf("The Radioactive Dwarf");break;
case -10:bprintf("The Heavy-Fan Dwarf");break;
case -13:bprintf("The Upper Class Dwarven Smith");break;
case -14:bprintf("The Singing Dwarf");break;
case -30:bprintf("The Sorceror");break;
case -31:bprintf("the Acolyte");break;
       default:
         bprintf("The Cardboard Box");
          break;
          }
    }
fpbn(name)
char *name;
{
long s;
extern char wd_them[],wd_him[],wd_her[],wd_it[];
s=fpbns(name);
if(s==-1) return(s);
if(!seeplayer(s)) return(-1);
return(s);
}

 fpbns(name)
 char *name;
    {
    char *n1[40],n2[40];
    long a;
    a=0;
    while(a<48)
       {
       strcpy(n1,name);strcpy(n2,PlayerCharacter.load(a).name);
       lowercase(n1);lowercase(n2);
if((!!strlen(n2))&&(!strcmp(n1,n2))) return(a);
       if(strncmp(n2,"the ",4)==0)
       if((!!strlen(n2))&&(!strcmp(n1,n2+4)))return(a);
       a++;
       }
    return(-1);
    }
 lispeople()
    {
    extern long debug_mode;
    extern long curch;
    extern long mynum;
    extern char wd_him[],wd_her[];
    long a,b;
    b=0;
    a=0;
    while(a<48)
       {
       if(a==mynum)
          {
          a++;
          continue;
          }
       if((PlayerCharacter.load(a).exists)&&(PlayerCharacter.load(a).channel_id==curch)&&(seeplayer(a)))
          {
          b=1;
         bprintf("%s ",PlayerCharacter.load(a).name);
         if(debug_mode) bprintf("{%d}",a);
          disl4(plev(a),PlayerCharacter.load(a).sex);
          if(PlayerCharacter.load(a).sex == PlayerCharacter.FEMALE) strcpy(wd_her,PlayerCharacter.load(a).name);
          else strcpy(wd_him,PlayerCharacter.load(a).name);
         bprintf(" is here carrying\n");
          lobjsat(a);
          }
       a++;
       }
    }
 
usercom()
{
extern long my_lev;
long a;
a=my_lev;
my_lev=0;
whocom();
my_lev=a;
}
 
oplong(x)
{
extern long debug_mode;
if(debug_mode) 
{
	bprintf("{%d} %s\n",x,Item.load(x).get_description(state(x)));	
	return;
}
if(strlen(Item.load(x).get_description(state(x))))
   bprintf("%s\n",Item.load(x).get_description(state(x)));
}

"""
