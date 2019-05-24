"""
Two Phase Game System
"""
import logging
from services.errors import CrapupError
from services.mud_exe import MudExeServices
from ..bbc import BBC
from ..tk import Talker


class GameStopped(Exception):
    pass


class CloseException(Exception):
    pass


class StopException(Exception):
    pass


class QuitException(Exception):
    pass


class ContinueException(Exception):
    pass


class GameGo:
    def __init__(self, *args):
        if len(args) != 2:
            raise Exception("Args!")

        self.services = MudExeServices
        self.args = args
        """
        char privs[4];
        """
        self.title, user = args
        username = user.get('username')
        username = "The {}".format(username) if username in ["Phantom"] else username
        user_id = user.get('user_id')

        logging.debug("mud.exe %s %s", self.title, username)

        # Extra
        self.in_fight = None
        self.pr_due = None

        print("Entering Game ....")

        self.signals = Signals(
            on_custom=self.on_custom(),
            on_error=self.on_error(),
            on_exit=self.on_exit(),
        )
        self.bbc = BBC(0)
        print("Hello {}".format(username))
        self.services.post_log("GAME ENTRY: {}[{}]".format(username, user_id))
        self.talker = Talker(
            username,
            on_loose=self.signals.alarm_off,
            on_before_buffer=self.signals.alarm_block,
            on_after_buffer=self.signals.alarm_unblock,
        )

    def on_error(self):
        def f(signals):
            signals.alarm_off()
            self.talker.loseme()
            self.bbc.disconnect()
            raise GameStopped(255)
        return f

    def on_exit(self):
        def f(signals):
            print("^C")
            if self.in_fight:
                return
            signals.alarm_off()
            self.talker.loseme()
            raise CrapupError("Byeeeeeeeeee  ...........")
        return f

    def on_custom(self):
        def f(signals):
            """

            :param signals:
            :return:
            """
            if not signals.active:
                return

            signals.alarm_off()
            self.talker.on_time()
            self.talker.pbfr(False)
            if self.talker.is_dirty():
                self.bbc.reprint()
            signals.alarm_on()
        return f

    def play(self):
        """

        :return:
        """
        while True:
            try:
                self.talker.show()
                self.signals.on_time()
            except KeyboardInterrupt as e:
                self.signals.on_exit(e)
            except ValueError as e:
                self.signals.on_kill(e)
            except SystemExit as e:
                self.signals.on_kill(e)
            except CloseException as e:
                self.signals.on_close(e)
            except StopException as e:
                self.signals.on_stop(e)
            except QuitException as e:
                self.signals.on_quit(e)
            except ContinueException as e:
                self.signals.on_continue(e)
            except CrapupError as e:
                self.game_over(e)
            except GameStopped as e:
                return e

    def game_over(self, message):
        """

        :param message:
        :return:
        """
        dashes = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        self.talker.pbfr()
        self.pr_due = 0  # So we dont get a prompt after the exit
        self.bbc.disconnect()

        print()
        print(dashes)
        print()
        print(message)
        print()
        print(dashes)
        raise GameStopped(0)


"""
listfl(name)
char *name;
{
FILE *a;
char b[128];
a=openlock(name,"r+");
while(fgets(b,128,a)) printf("%s\n",b);
fcloselock(a);
}
 
char *getkbd(s,l)   /* Getstr() with length limit and filter ctrl */
 char *s;
 int l;
    {
    char c,f,n;
    f=0;c=0;
    while(c<l)
       {
       regec:n=getchar();
       if ((n<' ')&&(n!='\n')) goto regec;
       if (n=='\n') {s[c]=0;f=1;c=l-1;}
       else
          s[c]=n;
       c++;
       }
    if (f==0) {s[c]=0;while(getchar()!='\n');}
    return(s);
    }
"""


"""
long interrupt=0;
"""


class Signals:
    def __init__(
        self,
        on_error=lambda signals: None,
        on_exit=lambda signals: None,
        on_custom=lambda signals: None,
    ):
        self.on_oops = on_error
        self.on_ctrlc = on_exit
        self.on_custom = on_custom
        self.on_alarm = lambda signals: None

        self.active = False

        self.__alarm = None

    def alarm_unblock(self):
        self.on_alarm = self.on_custom
        if self.active:
            self.__alarm = 2

    def alarm_block(self):
        self.on_alarm = lambda signals: None

    def alarm_on(self):
        self.active = True
        self.alarm_unblock()

    def alarm_off(self):
        self.active = False
        self.alarm_block()
        self.__alarm = 2147487643

    def on_close(self, e=None):
        logging.debug('SIGHUP: %s', e)
        self.on_oops(self)

    def on_exit(self, e=None):
        logging.debug('SIGINT: %s', e)
        self.on_ctrlc(self)

    def on_kill(self, e=None):
        logging.debug('SIGTERM: %s', e)
        self.on_ctrlc(self)

    @classmethod
    def on_stop(cls, e=None):
        logging.debug('SIGTSTP: %s', e)

    @classmethod
    def on_quit(cls, e=None):
        logging.debug('SIGQUIT: %s', e)

    def on_continue(self, e=None):
        logging.debug('SIGCONT: %s', e)
        self.on_oops(self)

    def on_time(self, e=None):
        logging.debug('alarm: %s', self.__alarm)
        logging.debug('SIGALRM: %s', e)
        self.on_alarm(self)


"""
set_progname(n,text)
char *text;
{
	/*
	int x=0;
	int y=strlen(argv_p[n])+strlen(argv_p[1]);  
	y++;
	if(strcmp(argv_p[n],text)==0) return;
	
	while(x<y)
	   argv_p[n][x++]=0; 
	strcpy(argv_p[n],text);
	*/
}

"""