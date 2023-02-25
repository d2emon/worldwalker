class Events:
    def __init__(self, events=None):
        self.events = events or {}
        self.listeners = []

    def emit(self, event_type, *args, **kwargs):
        for listener in self.listeners:
            listener.emit(event_type, *args, **kwargs)

        print(event_type, self.events)
        handler = self.events.get(event_type)
        if not handler:
            return
        return handler(event_type, *args, **kwargs)

    def update(self, events):
        self.events.update(events)
