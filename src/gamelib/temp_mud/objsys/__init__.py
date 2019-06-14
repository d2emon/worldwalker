"""
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