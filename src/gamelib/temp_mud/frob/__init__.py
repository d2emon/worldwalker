"""
frobnicate()
{
	extern char wordbuf[];
	int x;
	char ary[128];
	char bf1[8],bf2[8],bf3[8];
	if(not user.is_god)
	{
		bprintf("No way buster.\n");
		return;
	}
	if(brkword()==-1)
	{
		bprintf("Frobnicate who ?\n");
		return;
	}
	x=parser.user.find(wordbuf);
	if((x>15)&&(user.level!=10033))
	{
		bprintf("Can't frob mobiles old bean.\n");
		return;
	}
	if((Player(x).is_god)&&(user.level!=10033))
	{
		bprintf("You can't frobnicate %s!!!!\n",Player(x).name);
		return;
	}
	bprintf("New Level: ");
	pbfr();
	keysetback();
	getkbd(bf1,6);
	bprintf("New Score: ");
	pbfr();
	getkbd(bf2,8);
	bprintf("New Strength: ");
	pbfr();
	getkbd(bf3,8);
	keysetup();
	sprintf(ary,"%s.%s.%s.",bf1,bf2,bf3);
          World.load()
	user.send_message(Player(x).name,Player(x).name,-599,0,ary);
	bprintf("Ok....\n");
}


"""