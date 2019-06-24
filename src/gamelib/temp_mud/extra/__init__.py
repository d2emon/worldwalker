"""
 wizlist()
 {
 if(not user.is_wizard)
 {
 bprintf("Huh ?\n");
 return;
 }
          World.save()
 bprintf("\001f%s\001",WIZLIST);
 }

 incom()
 {
 extern char wordbuf[];
 char st[80],rn[80],rv[80];
 long ex_bk[7];
 long a;
 long x;
 long y;
 FILE *unit;
 a=0;
 if(not user.is_wizard){bprintf("Huh\n");return;}
 while(a<7)
 {
 ex_bk[a]=user.location.exits[a];
 a++;
 }
 if(brkword()== -1)
 {
 bprintf("In where ?\n");
 return;
 }
 strcpy(rn,wordbuf);
 if(brkword()== -1)
 {
 bprintf("In where ?\n");
 return;
 }
 strcpy(rv,wordbuf);
 x = Location.find(user, rn, rv);
 if(x==0)
 {
 bprintf("Where is that ?\n");
 return;
 }
 getreinput(st);
 y=user.location_id;
 user.__location_id=x;
          World.save()
 unit=openroom(user.location_id,"r");
if(unit==NULL){user.location_id=y;bprintf("No such room\n");return;}
user.location.load_exits(unit)
 fclose(unit);
          World.load()
 gamecom(st);
          World.load()
 if(user.location_id==x)
 {
 a=0;
 while(a<7) {user.location.exits[a]=ex_bk[a];a++;}
 }
 user.__location_id=y;
 }
 smokecom()
 {
 lightcom();
 }

 jumpcom()
 {
 long a,b;
 extern long jumtb[];
 char ms[128];
 extern char globme[];
 a=0;
 b=0;
 while(jumtb[a])
 {
 if(jumtb[a]==user.location_id){b=jumtb[a+1];break;}
 a+=2;
 }
 if(b==0){bprintf("Wheeeeee....\n");
 return;}
 if((not user.is_wizard)&&((!Item(1).is_carried_by(user))||(Item(1).state==0)))
 {
 	user.__location_id=b;
 bprintf("Wheeeeeeeeeeeeeeeee  <<<<SPLAT>>>>\n");
 bprintf("You seem to be splattered all over the place\n");
 LooseError("I suppose you could be scraped up - with a spatula");
 }
 sprintf(ms,"\001s%s\001%s has just left\n\001",globme,globme);
 user.send_message(globme,globme,-10000,user.location_id,ms);
 sprintf(ms,"\001s%s\001%s has just dropped in\n\001",globme,globme);
 user.send_message(globme,globme,-10000,b,ms);
     user.location_id = b
 }

long jumtb[]={-643,-633,-1050,-662,-1082,-1053,0,0};

wherecom()
 {
 extern char wordbuf[];
 extern char globme[];
 long cha,rnd;
 extern long numobs;
 if(user.strength<10)
 {
 bprintf("You are too weak\n");
 return;
 }
 if(not user.is_wizard) user.strength -= 2;
 rnd = random_percent()
 cha=10*user.level;
if((Item(111).is_carried_by(user))||(Item(121).is_carried_by(user))||(Item(163).is_carried_by(user)))
   cha=100;
          World.save()
 if(rnd>cha)
 {
 bprintf("Your spell fails...\n");
 return;
 }
 cha=0;
 if(brkword()== -1)
 {
 bprintf("What is that ?\n");
 return;
 }
 rnd=0;
 while(cha<numobs)
 {
 if(!strcmp(Item(cha).name,wordbuf))
    {
    rnd=1;
if(user.is_god) bprintf("[%3d]",cha);
    bprintf("%16s - ",Item(cha).name);
    if((not user.is_wizard)&&(Item(cha).is_destroyed)) bprintf("Nowhere\n");
    else
       desrm(Item(cha).location, Item(cha).carry_flag);
    }
 cha++;
 }
 cha=parser.user.find(wordbuf);
 if(cha!= -1)
 {
 rnd++;
 bprintf("%s - ",Player(cha).name);
 desrm(Player(cha).location,0);
 }
 if(rnd) return;
 bprintf("I dont know what that is\n");
 }

 desrm(loc,cf)
 {
 FILE *a;
 FILE *unit;
 long b;
 long x[32];
 if((not user.is_wizard)&&(cf==0)&&(loc>-5))
 {
 bprintf("Somewhere.....\n");
 return;
 }
if(cf==3){
bprintf("In the %s\n",Item(loc).name);
return;
}
 if(cf>0)
 {
 bprintf("Carried by \001c%s\001\n",Player(loc).name);
 return;
 }
 unit=openroom(loc,"r");
 if(unit==NULL)
 {
 bprintf("Out in the void\n");
 return;
 }
 b=0;
 while(b++<7) getstr(unit,x);
 bprintf("%-36s",x);
if(user.is_wizard){
    bprintf(" | ");
   yield loc.get_name(user)

    }
else bprintf("\n");
 fclose(unit);
 }



edit_world()
{
	extern long numobs;
	extern char wordbuf[];
	extern long ublock[];
	extern long objinfo[];
	char a[80],b,c,d;
	extern long genarg();
	if(!user.test_bit(5))
	{
		bprintf("Must be Game Administrator\n");
		return;
	}
	if(brkword()==-1)
	{
		bprintf("Must Specify Player or Object\n");
		return;
	}
	if(!strcmp(wordbuf,"player")) goto e_player;
	if(strcmp(wordbuf,"object"))
	{
		bprintf("Must specify Player or Object\n");
		return;
	}
	b=getnarg(0,numobs-1);
	if(b==-1) return;
	c=getnarg(0,3);
	if(c==-1) return;
	d=getnarg(0,0);
	if(d==-1) return;
	objinfo[4*b+c]=d;
        bprintf("Tis done\n");
        return;
e_player:b=getnarg(0,47);
	if(b==-1) return;
	c=getnarg(0,15);
	if(c==-1) return;
	d=getnarg(0,0);
	if(d==-1) return;
	ublock[16*b+c]=d;
        bprintf("Tis done\n");
        return;
}

long getnarg(bt,to)
long bt,to;
{
	extern char wordbuf[];
	long x;
	if(brkword()==-1)
	{
		bprintf("Missing numeric argument\n");
		return(-1);
	}
	x=numarg(wordbuf);
	if(x<bt) {bprintf("Invalid range\n");return(-1);}
	if((to)&&(x>to)) {bprintf("Invalid range\n");return(-1);}
	return(x);
}

"""