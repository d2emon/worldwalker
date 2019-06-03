from .errors import CommandError


def bprintf(message):
    print(message)


class Action:
    wizard_only = None
    god_only = None

    @classmethod
    def validate(cls, user):
        if cls.god_only and not user.is_god:
            raise CommandError(cls.god_only)
        if cls.wizard_only and not user.is_wizard:
            raise CommandError(cls.wizard_only)
        return True

    @classmethod
    def action(cls, parser, user):
        raise NotImplementedError()

    @classmethod
    def execute(cls, parser, user):
        try:
            cls.validate(user)
            for message in cls.action(user, parser):
                bprintf(message)
        except CommandError as e:
            bprintf(e)
