from games.mud.exceptions import FileServiceError
from .file_services import Exe, ResetN, MotD


def __now():
    return 0


def __time_to_string(time):
    """
    Elapsed time and similar goodies

    :return:
    """

    def seconds(s):
        if s % 60 == 1:
            return "1 second"
        else:
            return "{} seconds.".format(s % 60)

    time = __now() - time

    if time > 24 * 60 * 60:
        return "Over a day!!!\n"  # Add a Day !
    if time < 60:
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


def get_message_of_the_day():
    return MotD.get_message()


def get_time():
    """
    Check for all the created at stuff

    We use stats for this which is a UN*X system call

    :return:
    """
    created = "This AberMUD was created:{}".format(Exe.get_created())
    try:
        elapsed = "Game time elapsed: " + __time_to_string(ResetN.get_time())
    except FileServiceError:
        elapsed = "AberMUD has yet to ever start!!!"

    return {
        'created': created,
        'elapsed': elapsed,
    }
