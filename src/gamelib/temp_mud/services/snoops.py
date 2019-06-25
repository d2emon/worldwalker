class SnoopsService:
    __SNOOP = "SNOOP"
    __snoops = {}

    @classmethod
    def get(cls, **kwargs):
        user = kwargs.get('user')
        snoop = cls.__snoops.get(user, [])
        cls.__snoops[user] = []
        return snoop

    @classmethod
    def push(cls, **kwargs):
        user = kwargs.get('user')
        message = kwargs.get('message')

        if cls.__snoops.get(user) is None:
            cls.__snoops[user] = []
        cls.__snoops[user].append(message)
