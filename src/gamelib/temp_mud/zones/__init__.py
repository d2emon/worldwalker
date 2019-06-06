"""
Zone based name generator
"""
from gamelib.temp_mud.actions.action import Action
from ..location import Location
from ..zone import Zone, ZONES


def roomnum(user, name, offset=1):
    zone = Zone.by_name(name)
    if zone is None:
        return 0

    user.set_wd_there(name, offset)

    if not offset:
        return -zone.location_id(1)

    return -zone.location_id(int(offset))


class Exits(Action):
    @classmethod
    def action(cls, parser, user):
        yield "Obvious exits are\n"

        exits = list(filter(lambda l: l < 0, user.location.exits))

        if not len(exits):
            yield "None....\n"
            return

        for direction_id, location_id in enumerate(exits):
            if location_id >= 0:
                continue
            direction = Location.directions[direction_id]
            yield direction
            if user.is_wizard:
                yield " : {}".format(Location(location_id).name)
            yield "\n"


class Loc(Action):
    wizard_only = "Oh go away, that's for wizards\n"

    @classmethod
    def action(cls, parser, user):
        yield "\nKnown Location Nodes Are\n\n"
        for zone_id, zone in enumerate(ZONES):
            yield zone.name
            if zone_id % 4 == 3:
                yield "\n"
        yield "\n"
