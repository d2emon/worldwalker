import logging
import uuid
from ..errors import CrapupError, FileServiceError
from ..file_services import Snoop


"""
int tocontinue(str,ct,x,mx)
 char *str;
 long ct;
 char *x;
 long mx;
    {
    long s;
    s=0;
    while(str[ct]!='\001')
       {
       x[s++]=str[ct++];
       }
    x[s]=0;
if(s>=mx)
{
syslog("IO_TOcontinue overrun");
strcpy(str,"");
crapup("Buffer OverRun in IO_TOcontinue");
}
    return(ct+1);
    }


int pfile(str,ct,file)
 char *str;
 FILE *file;
    {
    char x[128];
    ct=tocontinue(str,ct,x,128);
    if(Parser.debug_mode) fprintf(file,"[FILE %s ]\n",str);
    f_listfl(x,file);
    return(ct);
    }

int pndeaf(str,ct,file)
 char *str;
 FILE *file;
    {
    char x[256];
    extern long ail_deaf;
    ct=tocontinue(str,ct,x,256);
    if(!ail_deaf)fprintf(file,"%s",x);
    return(ct);
    }

 pcansee(str,ct,file)
 char *str;
 FILE *file;
    {
    char x[25];
    char z[257];
    long a;
    ct=tocontinue(str,ct,x,23);
    if not seeplayer(fpbns(x), Talker, New1)
       {
       ct=tocontinue(str,ct,z,256);
       return(ct);
       }
    ct=tocontinue(str,ct,z,256);
    fprintf(file,"%s",z);
    return(ct);
    }

 prname(str,ct,file)
 char *str;
 FILE *file;
    {
    char x[24];
    ct=tocontinue(str,ct,x,24);
    fprintf(file, x if seeplayer(fpbns(x), Talker, New1) else "Someone")
    return(ct);
    }


int pndark(str,ct,file)
 char *str;
 FILE *file;
    {
    char x[257];
    ct=tocontinue(str,ct,x,256);
    if not WeatherService.get_is_dark(Talker.__channel) and not New1.ail_blind:
        fprintf(file,"%s",x);
    return(ct);
    }


int ppndeaf(str,ct,file)
 char *str;
 FILE *file;
    {
    char x[24];
    extern long ail_deaf;
    long a;
    ct=tocontinue(str,ct,x,24);
    if(ail_deaf) return(ct);
    fprintf(file, x if seeplayer(fpbns(x), Talker, New1) else "Someone")
    return(ct);
    }

int  ppnblind(str,ct,file)
char *str;
FILE *file;
    {
    char x[24];
    long a;
    ct=tocontinue(str,ct,x,24);
    if(New1.ail_blind) return(ct);
    fprintf(file, x if seeplayer(fpbns(x), Talker, New1) else "Someone")
    return(ct);
    }


int pnotkb(str,ct,file)
 char *str;
 FILE *file;
    {
    extern long iskb;
    char x[128];
    ct=tocontinue(str,ct,x,127);
    if(iskb) return(ct);
    fprintf(file,"%s",x);
    return(ct);
    }

"""


class Buffer:
    def __init__(self):
        self.__data = ""

        self.__log_fl = None  # 0 = not logging

        self.__iskb = True

        self.is_dirty = False
        self.is_finished = True

        self.snoopd = None

        self.snoopt = None
        # self.__sntn = ""

    def __get_start(self, is_finished=True):
        if not self.__data:
            return ""

        self.is_dirty = True

        if not is_finished:
            self.is_finished = False
        if self.is_finished:
            return ""
        else:
            self.is_finished = True
            return "\n"

    def __get_log(self):
        if self.__log_fl is None:
            return

        self.__iskb = False
        self.__decode(self.__log_fl)

    def __get_snoop(self, name):
        try:
            with Snoop(user=name, permissions='a') as token:
                self.__iskb = False
                self.__decode(token)
        except FileServiceError:
            return

    def __get_main(self):
        self.__iskb = True
        return self.__decode(None)

    def __view_snoop(self, user):
        """

        :return:
        """
        try:
            if self.snoopt is None:
                return FileServiceError

            return Snoop.view(user)
            # x = self.snoopt
            # self.snoopt = None
            # pbfr()
            # self.snoopt = x
        except FileServiceError:
            return ""

    def __clear(self):
        self.__data = ''

    def __decode(self, file):
        """
        The main loop

        :return:
        """
        logging.debug("dcprnt(%s, %s)", self.__data, file)
        # ct = 0
        # while ct < len(self.__data):
        #     if self.__data[ct] != "\001":
        #         fputc(self.__data[ct], file)
        #         ct += 1
        #         continue
        #     ct += 1
        #     if self.__data[ct] == 'f':
        #         ct = pfile(self.__data, ct + 1, file)
        #         continue
        #     elif self.__data[ct] == 'd':
        #         ct = pndeaf(self.__data, ct + 1, file)
        #         continue
        #     elif self.__data[ct] == 's':
        #         ct = pcansee(self.__data, ct + 1, file)
        #         continue
        #     elif self.__data[ct] == 'p':
        #         ct = prname(self.__data, ct + 1, file)
        #         continue
        #     elif self.__data[ct] == 'c':
        #         ct = pndark(self.__data, ct + 1, file)
        #         continue
        #     elif self.__data[ct] == 'P':
        #         ct = ppndeaf(self.__data, ct + 1, file)
        #         continue
        #     elif self.__data[ct] == 'D':
        #         ct = ppnblind(self.__data, ct + 1, file)
        #         continue
        #     elif self.__data[ct] == 'l':
        #         ct = pnotkb(self.__data, ct + 1, file)
        #         continue
        #     else:
        #         self.__data = ''
        #         loseme()
        #         raise CrapupError("Internal $ control sequence error\n")
        return self.__data

    def get_all(self, is_finished=True):
        result = ""
        result += self.__get_start(is_finished)
        self.__get_log()
        # if buffer.snoopd is not None:
        #     self.__get_snoop(Player.players[buffer.snoopd].name)
        result += self.__get_main()
        # result += buffer.view_snoop(globme)

        self.__clear()  # Clear buffer
        return result

    def add_message(self, message, raw=False):
        if raw:
            self.__data += message
            return
        # Max 240 chars/msg
        if len(message) > 235:
            # syslog("Bprintf Short Buffer overflow")
            raise CrapupError("Internal Error in BPRINTF")
        # Now we have a string of chars expanded
        self.__quprnt(message)

    def __quprnt(self, message):
        """

        :param message:
        :return:
        """
        if len(self.__data) + len(message) < 4095:
            self.__data += message
            return

        self.__data = ""
        # loseme()
        # syslog("Buffer overflow on user {}".format(globme))
        raise CrapupError("PANIC - Buffer overflow")


class BufferService:
    buffers = dict()

    @classmethod
    def get_buffer(cls, buffer_id, is_finished=True):
        """

        :return:
        """
        logging.debug("%s:\tpbfr()", buffer_id)
        return cls.buffers[buffer_id].get_all(is_finished)

    @classmethod
    def get_dirty(cls, buffer_id):
        """

        :return:
        """
        result = cls.buffers[buffer_id].is_dirty
        cls.buffers[buffer_id].is_dirty = False
        return result

    @classmethod
    def post_new_buffer(cls):
        """

        :return:
        """
        try:
            buffer_id = uuid.uuid1()
            if cls.buffers.get(buffer_id):
                raise BufferError()
            cls.buffers[buffer_id] = Buffer()  # 4K of chars should be enough for worst case
            return buffer_id
        except BufferError:
            raise CrapupError("Out Of Memory")

    @classmethod
    def post_buffer(cls, buffer_id, message, raw=False):
        cls.buffers[buffer_id].add_message(message, raw)

    @classmethod
    def post_dirty(cls, buffer_id):
        cls.buffers[buffer_id].is_dirty = True

"""
void logcom()
    {
    extern FILE * log_fl;
    extern char globme[];
    if(getuid()!=geteuid()) {bprintf("\nNot allowed from this ID\n");return;}
    if(log_fl!=0)
       {
       fprintf(log_fl,"\nEnd of log....\n\n");
       fclose(log_fl);
       log_fl=0;
       bprintf("End of log\n");
       return;
       }
    bprintf("Commencing Logging Of Session\n");
    log_fl=fopen("mud_log","a");
    if(log_fl==0) log_fl=fopen("mud_log","w");
    if(log_fl==0)
       {
       bprintf("Cannot open log file mud_log\n");
       return;
       }
    bprintf("The log will be written to the file 'mud_log'\n");
    }

void quprnt(x)
 char *x;
    {
    }

void snoopcom()
    {
    FILE *fx;
    long x;
    if(my_lev<10)
       {
       bprintf("Ho hum, the weather is nice isn't it\n");
       return;
       }
    if(snoopt!=-1)
       {
       bprintf("Stopped snooping on %s\n",sntn);
       snoopt= -1;
       sendsys(sntn,globme,-400,0,"");
       }
    if(brkword()== -1)
       {
       return;
       }
    x=fpbn(wordbuf);
    if(x==-1)
       {
       bprintf("Who is that ?\n");
       return;
       }
    if(((my_lev<10000)&&(plev(x)>=10))||(ptstbit(x,6)))
       {
       bprintf("Your magical vision is obscured\n");
       snoopt= -1;
       return;
       }
    strcpy(sntn,pname(x));
    snoopt=x;
    bprintf("Started to snoop on %s\n",pname(x));
    sendsys(sntn,globme,-401,0,"");
    fx=opensnoop(globme,"w");
    fprintf(fx," ");
    fcloselock(fx);
    }

void chksnp()
{
if(snoopt==-1) return;
sendsys(sntn,globme,-400,0,"");
}

void setname(x)  /* Assign Him her etc according to who it is */
long x;
{
	if((x>15)&&(x!=fpbns("riatha"))&&(x!=fpbns("shazareth")))
	{
		strcpy(wd_it,pname(x));
		return;
	}
	if(psex(x)) strcpy(wd_her,pname(x));
	else strcpy(wd_him,pname(x));
	strcpy(wd_them,pname(x));
}
"""
