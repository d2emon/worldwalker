"""
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