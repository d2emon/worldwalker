"""
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