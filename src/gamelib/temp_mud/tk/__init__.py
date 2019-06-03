"""
AberMUD II   C

This game systems, its code scenario and design
are (C) 1987/88  Alan Cox,Jim Finnis,Richard Acott

This file holds the basic communications routines
"""

"""
Data format for mud packets
 
Sector 0
[64 words]
0   Current first message pointer
1   Control Word
Sectors 1-n  in pairs ie [128 words]
 
[channel][controlword][text data]
 
[controlword]
0 = Text
- 1 = general request
"""

class Tk:
    mode = 0


def broad(*args):
    raise NotImplementedError()


def loseme(*args):
    raise NotImplementedError()


def trapch(*args):
    raise NotImplementedError()


#
"""
 broad(mesg)
 char *mesg;
    {
extern long rd_qd;
char bk2[256];
long block[128];
rd_qd=1;
block[1]= -1;
strcpy(bk2,mesg);
block[2:126] = bk2[0:126]
user.send2(block);
}

tbroad(message)
char *message;
    {
    broad(message);
    }
    
 sysctrl(block,luser)
 long *block;
 char *luser;
    {
    gamrcv(block);
    }
long  bound=0;
long  tmpimu=0;
char  *echoback="*e";
char  *tmpwiz=".";/* Illegal name so natural immunes are ungettable! */
 
 split(block,nam1,nam2,work,luser)
 long *block;
 char *nam1;
 char *nam2;
 char *work;
 char *luser;
    {
    long wkblock[128],a;
    wkblock[0:126] = block[2:126]
    work[0:64] = block[64:64]
    a=scan(nam1,(char *)wkblock,0,"",".");
    scan(nam2,(char *)wkblock,a+1,"",".");
if((strncmp(nam1,"The ",4)==0)||(strncmp(nam1,"the ",4)==0))
{
if(!strcmp(lowercase(nam1+4),lowercase(luser))) return(1);
}
    return(!strcmp(lowercase(nam1),lowercase(luser)));
    }
 trapch(chan)
 long chan;
    {
extern long curch;
    extern long mynum;
    FILE *unit;
    extern long my_lev;
    if(my_lev>9) goto ndie;
    ndie:unit=openworld();
    setploc(mynum,chan);
    lookin(chan);
    }
 
long mynum=0;
 
 putmeon(name)
 char *name;
    {
    extern long mynum,curch;
    extern long maxu;
    long ct,f;
    FILE *unit;
    extern long iamon;
    iamon=0;
    unit=openworld();
    ct=0;
    f=0;
    if(fpbn(name)!= -1)
       {
       crapup("You are already on the system - you may only be on once at a time");
       }
    while((f==0)&&(ct<maxu))
       {
       if (!strlen(pname(ct))) f=1;
       else
          ct++;
       }
    if(ct==maxu)
       {
       mynum=maxu;
       return;
       }
    strcpy(pname(ct),name);
    setploc(ct,curch);
    setppos(ct,-1);
    setplev(ct,1);
    setpvis(ct,0);
    setpstr(ct,-1);
    setpwpn(ct,-1);
    setpsex(ct,0);
    mynum=ct;
iamon=1;
    }
 
 loseme(name)
 char *name;
    {
extern long iamon;
extern long mynum;
extern long zapped;
char bk[128];
extern char globme[];
FILE *unit;  
sig_aloff(); /* No interruptions while you are busy dying */
			/* ABOUT 2 MINUTES OR SO */
user.in_setup=0;
			   
unit=openworld();
    dumpitems();
if(pvis(mynum)<10000) {
sprintf(bk,"%s has departed from AberMUDII\n",globme);
sendsys(globme,globme,-10113,0,bk);
}
    pname(mynum)[0]=0;
    	closeworld();
if(!zapped) saveme();
    	chksnp();
    }
 
long lasup=0;

 update(name)
 char *name;
    {
    extern long mynum,cms;
    FILE *unit;
    long xp;
    extern long lasup;
    xp=cms-lasup;
    if(xp<0) xp= -xp;
    if(xp<10) goto noup;
    unit=openworld();
    setppos(mynum,cms);
    lasup=cms;
    noup:;
    }
 
 revise(cutoff)
 long cutoff;
    {
    char mess[128];
    long ct;
    FILE *unit;
    unit=openworld();
    ct=0;
    while(ct<16)
       {
       if((pname(ct)[0]!=0)&&(ppos(ct)<cutoff/2)&&(ppos(ct)!=-2))
          {
          sprintf(mess,"%s%s",pname(ct)," has been timed out\n");
          broad(mess);
          dumpstuff(ct,ploc(ct));
          pname(ct)[0]=0;
          }
       ct++;
       }
    }
 
 lookin(room)
 long room; /* Lords ???? */
    {
    extern char globme[];
    FILE *un1,un2;
    char str[128];
    long xxx;
    extern long brmode;
    extern long curmode;
    extern long ail_blind;
    long ct;
    extern long my_lev;
    closeworld();
    if(ail_blind)
    {
    	bprintf("You are blind... you can't see a thing!\n");
    }
    if(my_lev>9) showname(room);
    un1=openroom(room,"r");
    if (un1!=NULL)
    {
xx1:   xxx=0;
       lodex(un1);
       	if(isdark())
       	{
          		fclose(un1);
          		bprintf("It is dark\n");
                        openworld();
          		onlook();
          		return;
          	}
       while(getstr(un1,str)!=0)
          {
          if(!strcmp(str,"#DIE"))
             {
             if(ail_blind) {rewind(un1);ail_blind=0;goto xx1;}
             if(my_lev>9)bprintf("<DEATH ROOM>\n");
             else
                {
                loseme(globme);
                crapup("bye bye.....\n");
                }
             }
          else
{
if(!strcmp(str,"#NOBR")) brmode=0;
else
             if((!ail_blind)&&(!xxx))bprintf("%s\n",str);
          xxx=brmode;
}
          }
       }
    else
       bprintf("\nYou are on channel %d\n",room);
    fclose(un1);
    openworld();
    if(!ail_blind)
    {
	    lisobs();
	    if(curmode==1) lispeople();
    }
    bprintf("\n");
    onlook();
    }
 loodrv()
    {
    extern long curch;
    lookin(curch);
    }
 

long iamon=0;

userwrap()
{
extern char globme[];
extern long iamon;
if(fpbns(globme)!= -1) {loseme();syslog("System Wrapup exorcised %s",globme);}
}
"""