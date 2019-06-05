from .errors import CommandError


def bprintf(message):
    print(message)


class BaseAction:
    @classmethod
    def prepare(cls, parser, action):
        return action

    @classmethod
    def validate(cls, user):
        return True

    @classmethod
    def action(cls, parser, user):
        raise NotImplementedError()

    @classmethod
    def execute(cls, parser, user):
        try:
            cls.validate(user)
            bprintf(*cls.action(user, parser))
        except CommandError as e:
            bprintf(e)


class Action(BaseAction):
    wizard_only = None
    god_only = None

    @classmethod
    def prepare(cls, parser, action):
        if action == ".q":
            return ""  # Otherwise drops out after command
        elif not action:
            return ""
        elif action == "!":
            return parser.string_buffer
        return action

    @classmethod
    def validate(cls, user):
        if cls.god_only and not user.is_god:
            raise CommandError(cls.god_only)
        if cls.wizard_only and not user.is_wizard:
            raise CommandError(cls.wizard_only)
        return True


class Special(BaseAction):
    @classmethod
    def prepare(cls, parser, action):
        if not action:
            return
        if action[0] != ".":
            return
        return action[1:].lower()
