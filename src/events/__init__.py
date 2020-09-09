class Events:
    def __init__(self, events=None):
        self.events = events or {}

    def emit(self, event_type, *args, **kwargs):
        handler = self.events.get(event_type)
        if not handler:
            return
        return handler(event_type, *args, **kwargs)
