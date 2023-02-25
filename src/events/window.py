from . import Events


class WindowEvents(Events):
    INIT = 'WINDOW.INIT'
    UPDATE = 'WINDOW.UPDATE'
    DRAW = 'WINDOW.DRAW'

    def init_window(self):
        self.emit(self.INIT)

    def process_events(self, events):
        for event in events:
            self.emit(event.type, event=event)

        self.emit(self.UPDATE)
        self.emit(self.DRAW)
