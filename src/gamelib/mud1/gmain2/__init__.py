"""
Program starts Here!

This forms the main loop of the code, as well as calling
all the initialising pieces
"""
from services.errors import CrapupError
from services.mud1 import Mud1Services
from ..gmainstubs import GMainStubs, cls, getty
from ..gmlnk import quick_start, talker


class MudGame:
    def __init__(self, host, username=None):
        self.host = host
        self.service = Mud1Services(self.host)

        self.__user = None
        self.__username = username
        self.__name_given = bool(self.username)

        # lump = ''
        # usrnam = ''
        if self.username:
            GMainStubs.ttyt = 0

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value or input("By what name shall I call you ?\n*")[:15].strip()
        self.__name_given = False

        # Check for legality of names
        self.service.validate_username(self.__username)

    def get_user(self):
        return self.service.get_user(self.username)

    @property
    def namegiv(self):
        return self.__name_given

    @property
    def namegt(self):
        return self.__username

    @property
    def qnmrq(self):
        return self.__name_given

    @property
    def show_all(self):
        return not self.__name_given

    @property
    def quick_start(self):
        return self.__name_given

    def show_splash(self):
        print()
        print()
        print()
        print()

        if not self.show_all:
            return

        getty()
        time = self.service.get_time()

        cls()
        print()
        print("                         A B E R  M U D")
        print()
        print("                  By Alan Cox, Richard Acott Jim Finnis")
        print()
        print(time['created'])
        print(time['elapsed'])

    def show_message_of_the_day(self):
        if not self.show_all:
            return

        input(self.service.get_message_of_the_day())
        print()
        print()

    def __try_password(self, tries=0):
        try:
            password = input("\nThis persona already exists, what is the password ?\n*")
            print()
            return self.service.auth(self.username, password)
        except PermissionError:
            if tries >= 2:
                raise CrapupError("\nNo!\n\n")
            return self.__try_password(tries + 1)

    def __set_password(self):
        try:
            password = input("*")
            print()
            return self.service.put_user(self.username, password)
        except ValueError as e:
            print(e)
            return self.__set_password()

    def login(self, username=None):
        """
        The whole login system is called from this

        Get the user name

        :return:
        """
        try:
            # Main login code
            self.username = username

            if self.get_user():
                return self.__try_password()

            # If he/she doesnt exist
            if input("\nDid I get the name right {} ?".format(self.username)).lower()[0] == 'n':
                raise ValueError()  # Check name

            # this bit registers the new user
            print("Creating new persona...")
            print("Give me a password for this persona")
            return self.__set_password()
        except ValueError as e:
            print(e)
            return self.login()

    def play(self):
        """
        The initial routine

        :return:
        """
        try:
            self.show_splash()
            # Does all the login stuff
            user = self.login(self.username)

            cls()
            self.show_message_of_the_day()
            self.service.put_log("Game entry by {} : UID {}".format(user.username, user.user_id))  # Log entry
            if self.quick_start:
                quick_start(user, self)
            else:
                talker(user, self)  # Run system
            self.game_over("Bye Bye")
        except CrapupError as e:
            self.game_over(e)

    @classmethod
    def game_over(cls, message):
        """
        Exit

        :param message:
        :return:
        """
        print()
        print(message)
        print()
        input("Hit Return to Continue...")
        raise SystemExit()


"""
/*
 *		This is just a trap for debugging it should never get
 *		called.
 */ 

void bprintf()
{
	printf("EEK - A function has trapped via the bprintf call\n");
	exit(0);
}
"""
