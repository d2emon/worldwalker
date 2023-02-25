class Events:
    def __init__(self, handlers=None):
        self.handlers = handlers or {}
        self.listeners = []

    def __send_to_listeners(self, event_type, *args, **kwargs):
        for listener in self.listeners:
            listener.emit(event_type, *args, **kwargs)

    def __handle(self, event_type, *args, **kwargs):
        handler = self.handlers.get(event_type)
        if not handler:
            return

        return handler(event_type, *args, **kwargs)

    def emit(self, event_type, *args, **kwargs):
        # print("EVENT", event_type, args, kwargs)
        self.__send_to_listeners(event_type, *args, **kwargs)
        self.__handle(event_type, *args, **kwargs)

    def update(self, events):
        self.handlers.update(events)
