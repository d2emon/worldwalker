"""
 getobj()
    {
    extern char globme[];
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
if(Item(113).is_destroyed) a=113;
else if(Item(114).is_destroyed) a=114;
if((a==113)||(a==114)) Item(a).clear_bit(0);
else bprintf("The shields are all to firmly secured to the walls\n");
}
    if(Item(a).flannel==1)
       {
      bprintf("You can't take that!\n");
       return;
       }
if(dragget()) return;
    if(user.overweight)
       {
      bprintf("You can't carry any more\n");
       return;
}
if((a==32)&&(state(a)==1)&&(user.helper is None))
{
	bprintf("Its too well embedded to shift alone.\n");
	return;
}
    Item(a).set_location(user,1);
    sprintf(bf,"\001D%s\001\001c takes the %s\n\001",globme,Item(a).name);
   bprintf("Ok...\n");
    user.send_message(globme,globme,-10000,user.location_id,bf);
if(Item(a).test_bit(12)) setstate(a,0);
if(user.location_id==-1081) 
{
	setstate(20,1);
	bprintf("The door clicks shut....\n");
}
    }

 ishere(item)
    {
    long a;
extern long my_lev;
    if((my_lev<10)&&(Item(item).is_destroyed))return(0);
    if(Item(item).carry_flag==1) return(0);
    if(Item(item).location!=user.location_id) return(0);
    return(1);
    }

 iscarrby(item,user)
    {
extern long my_lev;
    if((my_lev<10)&&(Item(item).is_destroyed))return(0);
    if((Item(item).carry_flag!=1)&&(Item(item).carry_flag!=2)) return(0);
    if(Item(item).location!=user) return(0);
    return(1);
    }

 dropitem()
    {
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
    Item(a).set_location(user.location_id,0);
   bprintf("OK..\n");
    sprintf(bf,"\001D%s\001\001c drops the %s.\n\n\001",globme,wordbuf);
    user.send_message(globme,globme,-10000,user.location_id,bf);
    if((user.location_id!=-183)&&(user.location_id!=-5))return;
   sprintf(bf,"The %s disappears into the bottomless pit.\n",wordbuf);
   bprintf("It disappears down into the bottomless pit.....\n");
    user.send_message(globme,globme,-10000,user.location_id,bf);
    my_sco+=(tscale()*Item(a).base_value)/5;
        yield from user.update()
Item(a).set_location(-6,0);
    }
 lisobs()
    {
    lojal2(1);
    yield from user.location.weather_description()
    lojal2(0);
    }

 lojal2(n)
    {
    extern char wd_it[];
    long a;
    a=0;
    while(a<NOBS)
       {
       if((ishere(a))&&(Item(a).flannel==n))
          {
              if(state(a)>3) continue;
              if(!!strlen(Item(a).description()))) /*OLONGT NOTE TO BE ADDED */
		{
			if(Item(a).is_destroyed) bprintf("--");
 
				oplong(a);
		          strcpy(wd_it,Item(a).name);
		}
          }
       a++;
       }
    }
 dumpitems()
    {
    dumpstuff(user,user.location_id);
    }

 dumpstuff(n,loc)
    {
    long b;
    b=0;
    while(b<NOBS)
       {
       if(iscarrby(b,n))

          {
          Item(b).set_location(loc,0);
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
       if(not Player(a).exists) goto npas;
       dispuser(a);
       npas:a++;
       }
   bprintf("\n");
    }

 dispuser(ubase)
    {
extern long my_lev;
    if(Player(ubase).is_dead) return; /* On  Non game mode */
    if(Player(ubase).visible >my_lev) return;
if(Player(ubase).visible) bprintf("(");
   bprintf("%s ",Player(ubase).name);
    disl4(Player(ubase).level, Player(ubase).sex);
if(Player(ubase).visible) bprintf(")");
if(Player(ubase).is_faded) bprintf(" [Absent From Reality]");
bprintf("\n");
    }

 disle3(n,s)
    {
    disl4(n,s);
   bprintf("\n");
    }
 disl4(n,s)
    {
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
case 19:if(!user.has_farted) bprintf("Of The Opera");
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
       strcpy(n1,name);strcpy(n2,Player(a).name);
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
    extern char wd_him[],wd_her[];
    long a,b;
    b=0;
    a=0;
    while(a<48)
       {
       if(a==user)
          {
          a++;
          continue;
          }
       if((Player(a).exists))&&(Player(a).location==user.location_id)&&(seeplayer(a)))
          {
          b=1;
         bprintf("%s ",Player(a).name);
         if(debug_mode) bprintf("{%d}",a);
          disl4(Player(a).level, Player(a).sex);
          if(Player(a).sex == Player.SEX_FEMALE) strcpy(wd_her,Player(a).name);
          else strcpy(wd_him,Player(a).name);
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
	bprintf("{%d} %s\n",x,Item(x).description());	
	return;
}
if(strlen(Item(x).description()))
   bprintf("%s\n",Item(x).description());
}

"""