import config.services
from games.mud.exceptions import MudError, FileServiceError
from .file_services import Nologin, BanFile, Exe, ResetN, MotD
from .file_services.person.person import Person
from . import logger


def now():
    return 0


def verify_host(f):
    def check_host(hostname):
        """
        Check we are running on the correct host
        see the notes about the use of flock();
        and the affects of lockf();

        :param hostname:
        :return:
        """
        if hostname != config.services.HOST_MACHINE:
            raise PermissionError("AberMUD is only available on {}, not on {}".format(config.services.HOST_MACHINE, hostname))

    def decorated(self, *args, **kwargs):
        check_host(self.hostname)
        Nologin.check()
        BanFile.check(self.user_id)

        return f(self, *args, **kwargs)
    return decorated


class Mud1Services:
    hostname = config.services.HOST_MACHINE

    def __init__(self, user_id):
        self.user_id = user_id

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

        time = now() - time

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

    @verify_host
    def delete_user(self, username):
        """
        For delete and edit

        :param username:
        :return:
        """
        return Person.delete(username)

    @verify_host
    def get_auth(self, username, password):
        return Person.auth(username, password)

    @verify_host
    def get_message_of_the_day(self):
        return MotD.get_message()

    @verify_host
    def get_time(self):
        """
        Check for all the created at stuff

        We use stats for this which is a UN*X system call

        :return:
        """
        created = "This AberMUD was created:{}".format(Exe.get_created())
        try:
            elapsed = "Game time elapsed: " + self.__time_string(ResetN.get_time())
        except FileServiceError:
            elapsed = "AberMUD has yet to ever start!!!"

        return {
            'created': created,
            'elapsed': elapsed,
        }

    @verify_host
    def get_user(self, username):
        """
        Return block data for user or -1 if not exist

        :param username:
        :return:
        """
        return Person.find(username)

    @verify_host
    def get_validate_password(self, value):
        return Person.validate_username(value)

    @verify_host
    def get_validate_username(self, value):
        return Person.validate_password(value)

    @verify_host
    def post_log(self, message):
        logger.post(message)

    @verify_host
    def post_user(self, username, password):
        try:
            return Person(self.user_id, username, password).add()
        except FileServiceError:
            raise MudError("No persona file....\n")

    @verify_host
    def put_password(self, username, old_password, new_password):
        Person.auth(username, old_password)
        return self.put_user(username, new_password)

    @verify_host
    def put_user(self, username, password):
        try:
            # delete me and tack me on end!
            self.delete_user(username)
            return Person(self.user_id, username, password).add()
        except FileServiceError:
            return
