import config.services
from games.mud.exceptions import FileServiceError
from .file_services import Nologin, BanFile
from .file_services.person.person import Person


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

    def check_nologin():
        Nologin.check()

    def check_banned(user_id):
        BanFile.check(user_id)

    def decorated(host_id, user_id, *args, **kwargs):
        check_host(host_id)
        check_nologin()
        check_banned(user_id)
        return f(*args, **kwargs)

    return decorated


@verify_host
def get_auth(username, password):
    return Person.auth(username, password)


@verify_host
def get_user(username):
    """
    Return block data for user or -1 if not exist

    :param username:
    :return:
    """
    return Person.find(username)


@verify_host
def post_user(user_id, username, password):
    return Person(user_id, username, password).add()


@verify_host
def put_user(user_id, username, password):
    try:
        # delete me and tack me on end!
        __delete_user(username)
        return Person(user_id, username, password).add()
    except FileServiceError:
        return


@verify_host
def validate(field, value):
    if field == 'username':
        return Person.validate_username(value)
    elif field == 'password':
        return Person.validate_password(value)


@verify_host
def put_password(username, old_password, new_password):
    Person.auth(username, old_password)
    return put_user(username, new_password)


@verify_host
def delete_user(username):
    """
    For delete and edit

    :param username:
    :return:
    """
    return Person.delete(username)
