from . import config
from .errors import CrapupError, FileServiceError
from .file_services import Nologin, Exe, ResetN, MotD, BanFile, Pfl, Pft, LogFile
from .file_services.person.person import Person
from .utils import encode, decode


class Mud1Services:
    def __init__(self, host):
        self.host = host

    @classmethod
    def __add_user(cls, user_id, username, password):
        user = Person(user_id, username, password)
        token = Pfl.connect(lock=True, permissions="a")
        Pfl.add_line(token, encode(user))
        Pfl.disconnect(token)
        return user

    @classmethod
    def __validate_host(cls, host):
        """
        Check we are running on the correct host
        see the notes about the use of flock();
        and the affects of lockf();

        :param host:
        :return:
        """
        if host != config.HOST_MACHINE:
            raise PermissionError("AberMUD is only available on {}, not on {}".format(config.HOST_MACHINE, host))

    @classmethod
    def __check_nologin(cls):
        """
        Check if there is a no logins file active

        :return:
        """
        try:
            token = Nologin.connect(permissions='r')
            error = Nologin.get_content(token)
            Nologin.disconnect(token)
            raise error
        except FileServiceError:
            return

    def __check_banned(self, host_id):
        """
        Check to see if UID in banned list

        :return:
        """
        try:
            token = BanFile.connect(permissions="r+")
            for banned in BanFile.get_line(token, max_length=79):
                if banned == host_id:
                    raise PermissionError("I'm sorry- that userid has been banned from the Game\n")
            BanFile.disconnect(token)
        except FileServiceError:
            return

    @classmethod
    def __time_string(cls, time):
        """
        Elapsed time and similar goodies

        :return:
        """
        def seconds(s):
            if s % 60 == 1:
                return "1 second"
            else:
                return "{} seconds.".format(s % 60)

        if time > 24 * 60 * 60:
            return "Over a day!!!\n"  # Add a Day !
        if time < 61:
            return seconds(time)
        if time == 60:
            return "1 minute"
        if time < 120:
            return "1 minute and " + seconds(time)
        if time / 60 == 60:
            return "1 hour"
        if time < 120:
            return "{} minutes and ".format(time / 60) + seconds(time)

        if time < 7200:
            hours = "1 hour and "
        else:
            hours = "{} hours and ".format(time / 3600)

        if (time / 60) % 60 != 1:
            return hours + "{} minutes.".format((time / 60) % 60)
        else:
            return hours + "1 minute"

    def __verify_host(self):
        self.__validate_host(self.host.hostname)
        self.__check_nologin()
        # Check if banned first
        self.__check_banned(self.host.host_id)

    def auth(self, username, password):
        self.__verify_host()

        user = self.get_user(username)
        if user is None:
            raise PermissionError()
        if password != user.password:
            raise PermissionError()

    def delete_user(self, username):
        """
        For delete and edit

        :param username:
        :return:
        """
        self.__verify_host()

        search = username.lower()
        user = self.get_user(search)
        if user is None:
            raise ValueError("\nCannot delete non-existant user")

        try:
            token_a = Pfl.connect_lock(permissions="r+")
            token_b = Pft.connect_lock(permissions="w")
            for user in Pfl.get_content(token_a):
                if decode(user).username.lower() != search:
                    Pft.add_line(token_b, user)
            Pfl.disconnect(token_a)
            Pft.disconnect(token_b)

            token_a = Pfl.connect_lock(permissions="w")
            token_b = Pft.connect_lock(permissions="r+")
            for user in Pft.get_content(token_b):
                Pfl.add_line(token_a, user)
            Pfl.disconnect(token_a)
            Pft.disconnect(token_b)

        except FileServiceError:
            return

    def get_time(self):
        """
        Check for all the created at stuff

        We use stats for this which is a UN*X system call

        :return:
        """
        self.__verify_host()

        stats = Exe.get_stats()
        token = ResetN.connect(permissions='r')
        time = ResetN.time(token)

        created = stats.date if stats is not None else "<unknown>\n"
        try:
            elapsed = "Game time elapsed: " + self.__time_string(time)
        except FileServiceError:
            elapsed = "AberMUD has yet to ever start!!!"

        return {
            'created': "This AberMUD was created:{}".format(created),
            'elapsed': elapsed,
        }

    def get_message_of_the_day(self):
        self.__verify_host()

        try:
            return MotD.get_text()  # list the message of the day
        except FileServiceError as e:
            return e

    def get_user(self, username, default=False):
        """
        Return block data for user or -1 if not exist

        :param default:
        :param username:
        :return:
        """
        self.__verify_host()

        try:
            token = Pfl.connect(lock=True, permissions="r")
            found = None
            search = username.lower()
            for user in Pfl.get_content(token):
                decoded = decode(user)
                if decoded.username.lower() == search:
                    found = decoded
                    break
            Pfl.disconnect(token)

            if found is None and default:
                return Person(
                    self.host.host_id,
                    username,
                    "default",
                    # "E"
                )
            return found
        except FileServiceError:
            raise CrapupError("No persona file\n")

    def put_log(self, message):
        try:
            LogFile.log(message)
        except FileServiceError:
            # loseme()
            raise CrapupError("Log fault : Access Failure")

    def put_password(self, username, old_password, new_password):
        self.__verify_host()

        self.auth(username, old_password)
        self.update_user(username, new_password)

    def put_user(self, username, password):
        self.__verify_host()

        try:
            return self.__add_user(self.host.host_id, username, password)
        except FileServiceError:
            raise CrapupError("No persona file....\n")

    def update_user(self, username, password):
        self.__verify_host()

        try:
            self.delete_user(username)  # delete me and tack me on end!
            return self.__add_user(self.host.host_id, username, password)
        except FileServiceError:
            return

    def validate_password(self, value):
        self.__verify_host()

        return Person.validate_username(value)

    def validate_username(self, value):
        self.__verify_host()

        return Person.validate_password(value)

    def execute(self, *args):
        self.__verify_host()

        print("\texecl({}".format(args))

    def run_game(self, *args):
        self.__verify_host()

        try:
            self.execute(Exe, *args)
        except FileServiceError:
            raise CrapupError("mud.exe : Not found\n")