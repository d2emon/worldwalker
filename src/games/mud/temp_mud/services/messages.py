class MessagesService:
    __first_message_id = 0
    __last_message_id = 0
    __messages = {}
    __MAX_MESSAGES = 199

    @classmethod
    def __get_message_id(cls, **kwargs):
        message_id = kwargs.get('message_id')
        # return 2 * message_id - cls.first_message
        return message_id

    @classmethod
    def __get_new_message_id(cls):
        # return cls.__get_message_id(message_id=cls.__last_message_id) + 1
        return cls.__last_message_id + 1

    @classmethod
    def __on_overflow(cls):
        # World.load()
        cls.__first_message_id += 100
        for message_id in [message_id for message_id in cls.__messages.keys() if message_id < cls.__first_message_id]:
            del cls.__messages[message_id]

    @classmethod
    def post(cls, **kwargs):
        message = kwargs.get('message')

        # try:
        #     # World.load()
        # except ServiceError:
        #     raise LooseError("\nAberMUD: FILE_ACCESS : Access failed\n")

        message_id = cls.__get_new_message_id()
        cls.__messages[message_id] = message
        cls.__last_message = message_id

        overflow = message_id >= cls.__MAX_MESSAGES
        if overflow:
            cls.__on_overflow()
        return {
            'result': True,
            'message_id': message_id,
            'overflow': overflow,
            'first_message_id': cls.__first_message_id,
            'last_message_id': cls.__last_message_id,
        }

    @classmethod
    def get(cls, **kwargs):
        first = kwargs.get('first')
        last = kwargs.get('last')
        message_id = kwargs.get('message_id')

        if message_id is not None:
            return {
                'result': True,
                'message': cls.__messages[message_id],
            }

        # try:
        #     World.load()
        # except ServiceError:
        #     raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")
        if last is None:
            last = cls.__last_message_id
        if first is None or first < 0:
            first = last
        return map(lambda i: cls.get(message_id=i), range(first, last))
