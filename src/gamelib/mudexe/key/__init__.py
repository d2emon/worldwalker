"""
Key drivers
"""


class Tc:
    __echo = True
    __i_canon = True

    @classmethod
    def get_attr(cls):
        return {
            'ECHO': cls.__echo,
            'ICANON': cls.__i_canon,
        }

    @classmethod
    def set_attr(cls, **kwargs):
        cls.__echo = kwargs.get('ECHO', cls.__echo)
        cls.__i_canon = kwargs.get('ICANON', cls.__i_canon)


class Key:
    MODE_DEFAULT = 0
    MODE_NOT_DEFAULT = 1

    __save_flag = None

    __mode = MODE_DEFAULT
    __prompt = ""
    __buffer = ""

    @classmethod
    def setup(cls):
        """

        :return:
        """
        flags = Tc.get_attr()
        cls.save_flag = flags
        Tc.set_attr(
            ECHO=False,
            ICANON=False,
        )

    @classmethod
    def setback(cls):
        """

        :return:
        """
        Tc.set_attr(**cls.__save_flag)

    @classmethod
    def reprint(cls):
        """

        :return:
        """
        if cls.__mode != cls.MODE_NOT_DEFAULT:
            return
        print()
        print("{}{}".format(cls.__prompt, cls.__buffer), end="")


"""
key_input(ppt,len_max)
char *ppt;
int len_max;
{
   char x;
   extern long pr_due;
   int len_cur=0;
   key_mode=0;
   strcpy(pr_bf,ppt);
   bprintf("%s",ppt);
   pbfr();
   pr_due=0;
   strcpy(key_buff,"");
   while(len_cur<len_max)
   {
   	x=getchar();
   	if(x=='\n')
   	{
   		printf("\n");
   		key_mode= -1;
    		return;
   	}
   	if(((x==8)||(x==127))&&(len_cur))
	{
		putchar(8);
		putchar(' ');
		putchar(8);
		len_cur--;
		key_buff[len_cur]=0;
		continue;
	}
	if(x<32) continue;
	if(x==127) continue;
	putchar(x);
	key_buff[len_cur++]=x;
	key_buff[len_cur]=0;
     }
}	
"""