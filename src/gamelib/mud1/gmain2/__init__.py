"""
Program starts Here!

This forms the main loop of the code, as well as calling
all the initialising pieces
"""
from services.errors import CrapupError
from services.mud1 import Mud1Services
from ..gmainstubs import GMainStubs, getty
from ..gmlnk import quick_start, talker
from ..screens import Splash, LoginScreen, MessageOfTheDay, GameOver


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
        self.__name_given = False
        username = value or LoginScreen.input_username()

        # Check for legality of names
        self.__username = self.service.validate_username(username)

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
        getty()
        time = self.service.get_time()
        Splash.show(
            visible=self.show_all,
            created=time['created'],
            elapsed=time['elapsed'],
        )

    def show_message_of_the_day(self):
        MessageOfTheDay.show(
            visible=self.show_all,
            message=self.service.get_message_of_the_day()
        )

    def __try_password(self, tries=0):
        try:
            return self.service.auth(self.username, LoginScreen.input_password())
        except PermissionError:
            if tries >= 2:
                raise CrapupError("\nNo!\n\n")
            return self.__try_password(tries + 1)

    def __set_password(self):
        try:
            return self.service.put_user(self.username, LoginScreen.input_new_password())
        except ValueError as e:
            LoginScreen.show_message(e)
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
            if not LoginScreen.verify_username(username=self.username):
                raise ValueError()  # Check name

            # this bit registers the new user
            LoginScreen.new_user()
            return self.__set_password()
        except ValueError as e:
            LoginScreen.show_message(e)
            return self.login()

    def play(self):
        """
        The initial routine

        :return:
        """
        try:
            print()
            print()
            print()
            print()

            self.show_splash()
            # Does all the login stuff
            user = self.login(self.username)

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
        GameOver.show_message(message=message)
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
