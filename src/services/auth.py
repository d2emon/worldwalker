import config.services
from .file_services import Nologin, BanFile, User


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
def validate(**kwargs):
    return {field: User.validate(field, value) for field, value in kwargs.items()}


@verify_host
def post_user(**kwargs):
    return User(**kwargs).add()


@verify_host
def get_user(user_id):
    return User.by_username(user_id).as_dict()


@verify_host
def put_user(user_id, **kwargs):
    return User.by_username(user_id).update(**kwargs).save()


@verify_host
def delete_user(user_id):
    return User.by_username(user_id).delete()


@verify_host
def get_auth(username, password):
    return User.auth(username, password).as_dict()


@verify_host
def put_password(username, password, new_password):
    return User.auth(username, password).update(password=new_password).save()
