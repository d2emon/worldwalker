"""
Two Phase Game System
"""
import logging
from services.errors import CrapupError
from services.mud_exe import MudExeServices
from services.world import WorldService
from ..bbc import BBC
from ..tk import Talker
from .errors import GameStopped, CloseException, StopException, QuitException, ContinueException
from . import signals


class GameGo:
    def __init__(self, title, user):
        # Extra
        self.__in_fight = None

        # Game go
        self.services = MudExeServices
        self.user = user
        logging.debug("mud.exe %s %s", title, self.username)

        username = self.username
        print("Entering Game ....")
        self.bbc = BBC(
            tty=0,
            title=title,
            on_error=self.on_error,
            on_exit=self.on_exit,
            on_timer=self.on_timer,
        )
        print("Hello {}".format(username))
        self.services.post_log("GAME ENTRY: {}[{}]".format(username, self.user_id))
        self.talker = Talker(
            username,
            on_loose=self.on_loose,
            get_cmd=self.get_cmd,
            # show_buffer=self.bbc.show_buffer,
        )

    @property
    def user_id(self):
        return self.user.get('user_id')

    @property
    def username(self):
        username = self.user.get('username')
        return "The {}".format(username) if username in ["Phantom"] else username

    def play(self):
        while True:
            try:
                self.bbc.run(self.talker.show)
            except CrapupError as e:
                self.game_over(e)
            except GameStopped as e:
                return e

    def game_over(self, message):
        self.bbc.game_over()

        dashes = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        print()
        print(dashes)
        print()
        print(message)
        print()
        print(dashes)
        raise GameStopped(0)

    # Events
    def on_error(self):
        self.talker.loseme()
        self.bbc.disconnect()
        raise GameStopped(255)

    def on_exit(self):
        print("^C")
        if self.__in_fight:
            return

        self.talker.loseme()
        raise CrapupError("Byeeeeeeeeee  ...........")

    def on_timer(self):
        with WorldService():
            self.bbc.events.interrupt = True
            # self.talker.rte(interrupt=self.bbc.events.interrupt)
            self.talker.rte()
            self.bbc.events.interrupt = False
            # self.talker.on_time()
            on_timing()
        self.bbc.reprint()

    # Talker events
    def __show_bottom(self):
        self.bbc.show_buffer()
        self.bbc.show_bottom_screen()

    def get_cmd(self):
        self.__show_bottom()

        prompt = self.talker.prompt
        self.bbc.show_buffer()

        if self.talker.player.visible > 9999:
            self.bbc.title = "-csh"
        elif self.talker.player.visible == 0:
            self.bbc.title = "   --}----- ABERMUD -----{--     Playing as {}".format(self.username)

        self.bbc.events.is_active = True
        # work = key_input(prompt, 80)
        self.bbc.events.is_active = False

        self.bbc.show_top_screen()
        sysbuf += "<l>{}<\l>".format(work)

        with WorldService():
            self.talker.rte()

        if self.talker.__conv_flg and work = "**"
            self.talker.__conv_flg = 0
            return self.get_cmd

        if not work:
            return nadj()
        if work != "*" and work[0] == "*":
            work[0] = 32
            return nadj()
        if self.talker.__conv_flg:
            w2 = work
            if self.talker.__conv_flg == 1:
                work = "say {}"
            else:
                work = "tss {}"

        if work == "&"
    """
        if((strcmp(work,"*"))&&(work[0]=='*')){(work[0]=32);goto nadj;}
        if(convflg)
        {
            strcpy(w2,work);
            if(convflg==1) sprintf(work,"say %s",w2);
            else
                sprintf(work,"tss %s",w2);
        }
        """
        """
        nadj:if(curmode==1) gamecom(work);
        else
        {
            if(((strcmp(work,".Q"))&&(strcmp(work,".q")))&& (!!strlen(work)))
            {
                a=special(work,name);
            }
        }
        """
        """
        if(fighting>-1)
        {
            if(!strlen(pname(fighting))) 
            {
                in_fight=0;
                fighting= -1;
            }
            if(ploc(fighting)!=curch) 
            {
                in_fight=0;
                fighting= -1;
            }
        }
        if(in_fight) in_fight-=1;
        return((!strcmp(work,".Q"))||(!strcmp(work,".q")));
        
        :return: 
        """
        work = self.show_input()
        self.show_top()
        return self.talker.process_cmd(work)

    def on_loose(self):
        self.bbc.events.is_active = False

    def on_before_input(self, prompt):
        self.bbc.add_buffer(prompt)
        self.bbc.show_buffer()
        self.bbc.is_dirty = True

    # Unsorted
    def show_input(self):
        self.bbc.show_buffer()

        username = self.talker.player.name
        if self.talker.player.visible > 9999:
            self.bbc.title = "-csh"
        elif self.talker.player.visible == 0:
            self.bbc.title = "   --}}----- ABERMUD -----{{--     Playing as {}".format(username)

        self.bbc.events.is_active = True
        work = self.bbc.get_input(self.talker.prompt, on_input=self.on_before_input)
        self.bbc.events.on_timer()
        self.bbc.events.is_active = False

        return work

    def show_top(self):
        self.bbc.show_top_screen()
