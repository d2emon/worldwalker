from .action import Action
from ..location import Location
from ..zone import ZONES


class Exits(Action):
    # 136
    commands = "exits",

    @classmethod
    def action(cls, command, parser):
        yield "Obvious exits are\n"

        if not len(parser.user.location.visible_exits):
            yield "None....\n"
            return

        for direction_id, location_id in enumerate(parser.user.location.exits):
            if location_id >= 0:
                continue

            location = Location(location_id)
            yield location.directions[direction_id]
            if parser.user.is_wizard:
                yield " : {}".format(location.name)
            yield "\n"


class Loc(Action):
    # 153
    commands = "loc",
    wizard_only = "Oh go away, that's for wizards\n"

    @classmethod
    def action(cls, command, parser):
        yield "\nKnown Location Nodes Are\n\n"
        for zone_id, zone in enumerate(ZONES):
            yield zone.name
            if zone_id % 4 == 3:
                yield "\n"
        yield "\n"
