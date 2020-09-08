from .world import WorldService


def get_events(event_id=None):
    WorldService.connect()

    last_event_id = WorldService.get_last_message_id()
    first_event_id = event_id or last_event_id
    events = [WorldService.get_message(i) for i in range(first_event_id, last_event_id)]
    return event_id, events
