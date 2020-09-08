class CommandError(Exception):
    pass


class CrapupError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ServiceError(Exception):
    pass


class LooseError(CrapupError):
    pass