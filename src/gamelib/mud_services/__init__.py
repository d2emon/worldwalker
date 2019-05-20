from ..file_services import Nologin, Exe, ResetN, MotD, BanFile, Pfl
from ..mud1.errors import CrapupError
from . import config


class Mud1Services:
    @classmethod
    def validate_host(cls, host):
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
    def check_nologin(cls):
        """
        Check if there is a no logins file active

        :return:
        """
        try:
            token = Nologin.connect(permissions='r')
            error = Nologin.get_content(token)
            Nologin.disconnect(token)
            raise error
        except FileNotFoundError:
            return

    @classmethod
    def __show_time(cls, time):
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

    @classmethod
    def get_time(cls):
        """
        Check for all the created at stuff

        We use stats for this which is a UN*X system call

        :return:
        """
        stats = Exe.get_stats()
        token = ResetN.connect(permissions='r')
        time = ResetN.time(token)

        created = stats.date if stats is not None else "<unknown>\n"
        try:
            elapsed = "Game time elapsed: " + cls.__show_time(time)
        except FileNotFoundError:
            elapsed = "AberMUD has yet to ever start!!!"

        return {
            'created': "This AberMUD was created:{}".format(created),
            'elapsed': elapsed,
        }

    @classmethod
    def get_message_of_the_day(cls):
        try:
            return MotD.get_text()  # list the message of the day
        except Exception as e:
            return e

    @classmethod
    def chkbndid(cls, user_id):
        """
        Check to see if UID in banned list

        :return:
        """
        try:
            token = BanFile.connect(permissions="r+")
            for banned in BanFile.get_line(token, max_length=79):
                if banned == user_id:
                    raise PermissionError("I'm sorry- that userid has been banned from the Game\n")
            BanFile.disconnect(token)
        except FileNotFoundError:
            return

    @classmethod
    def validate_username(cls, username):
        if "." in username:
            raise CrapupError("\nIllegal characters in user name\n")

        if not username:
            raise ValueError

        chkname(username)

        try:
            validname(username)
        except ValueError:
            raise CrapupError("Bye Bye")

    @classmethod
    def logscan(cls, username):
        """
        Return block data for user or -1 if not exist

        :param username:
        :return:
        """
        try:
            token = Pfl.connect_lock(permissions="r")
            found = None
            for user in Pfl.get_content(token):
                decoded = dcrypt(user)
                if decoded.username.lower() == username.lower():
                    found = decoded
                    break
                else:
                    continue
            Pfl.disconnect(token)
            return found
        except FileNotFoundError:
            raise CrapupError("No persona file\n")
