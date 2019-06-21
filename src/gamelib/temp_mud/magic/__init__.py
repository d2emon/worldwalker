import random


def random_percent():
    return random.randrange(100)


"""
 goloccom()
    {
    extern char globme[];
    char n1[128];
    char bf[128];
    extern char mout_ms[],min_ms[];
    extern char wordbuf[];
    long a;
    FILE *b;
    if(not user.is_wizard)
       {
       bprintf("huh ?\n");
       return;
       }
    if(brkword()== -1)
       {
       bprintf("Go where ?\n");
       return;
       }
    strcpy(n1,wordbuf);
    if(brkword()== -1) strcpy(wordbuf,"");
    a=Location.find(user, n1, wordbuf);
    if((a>=0)||((b=openroom(a,"r"))==0))
       {
       bprintf("Unknown Room\n");
       return;
       }
    fclose(b);
    sprintf(bf,"\001s%%s\001%%s %s\n\001",mout_ms);
    user.silly(bf);
    user.location_id = a
    sprintf(bf,"\001s%%s\001%%s %s\n\001",min_ms);    
    user.silly(bf);
    }




 wizcom()
    {
    extern char globme[],wordbuf[];
    char bf[128];
    if(not user.is_wizard)
       {
       bprintf("Such advanced conversation is beyond you\n");
       return;
       }
    getreinput(wordbuf);
    sprintf(bf,"\001p%s\001 : %s\n",globme,wordbuf);
    user.send_message(globme,globme,-10113,user.location_id,bf);
    user.force_read = True
    }

 viscom()
    {
    long f;
    extern char globme[];
    long ar[4];
    if(not user.is_wizard)
       {
       bprintf("You can't just do that sort of thing at will you know.\n");
       return;
       }
    if(!user.visible)
       {
       bprintf("You already are visible\n");
       return;
       }
    user.visible = 0
    ar[0]=user;
    ar[1]=user.visible
    user.send_message("","",-9900,0,ar);
    bprintf("Ok\n");
    user.silly("\001s%s\001%s suddenely appears in a puff of smoke\n\001");
    }

 inviscom()
    {
    extern char globme[];
    extern char wordbuf[];
    long f,x;
    long ar[4];
    if(not user.is_wizard)
       {
       bprintf("You can't just turn invisible like that!\n");
       return;
       }
    x=10;
    if(user.is_god) x=10000;
    if((user.level==10033)&&(brkword()!=-1)) x=numarg(wordbuf);
    if(user.visible==x)
       {
       bprintf("You are already invisible\n");
       return;
       }
    user.visible = x
    ar[0]=user;
    ar[1]=user.visible
    user.send_message("","",-9900,0,ar);
    bprintf("Ok\n");
    user.silly("\001c%s vanishes!\n\001");
    }

 ressurcom()
    {
    long bf[32];
    long a,b;
    extern char wordbuf[];
    if(not user.is_wizard)
       {
       bprintf("Huh ?\n");
       return;
       }
    if(brkword()== -1)
       {
       bprintf("Yes but what ?\n");
       return;
       }
    a = Item.find(
        wordbuf,
        available=True,
        mode_0=True,
        destroyed=parser.user.is_wizard
    )
    if(a== -1)
       {
       bprintf("You can only ressurect objects\n");
       return;
       }
    if(not Item(a).is_destroyed)
       {
       bprintf("That already exists\n");
       return;
       }
    Item(a).create();
    Item(a).set_location(user.location_id,0);
    sprintf(bf,"The %s suddenly appears\n",Item(a).name);
    user.send_message("","",-10000,user.location_id,bf);
    }
"""