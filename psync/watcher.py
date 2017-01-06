from watchdog.events import FileSystemEventHandler


class AnyEventHandler(FileSystemEventHandler):
    def __init__(self, state):
        super(AnyEventHandler, self).__init__()
        # A dirty way to emit changes to the outside world.
        # Should try to use other pure way to do this.
        self.state = state

    def on_any_event(self, event):
        super(AnyEventHandler, self).on_any_event(event)
        self.state["dirty"] = True
