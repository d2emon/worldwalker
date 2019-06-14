"""
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