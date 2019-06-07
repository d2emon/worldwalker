"""
Zone based name generator
"""
from ..zone import Zone


def roomnum(user, name, offset=1):
    zone = Zone.by_name(name)
    if zone is None:
        return 0

    user.set_wd_there(name, offset)

    if not offset:
        return -zone.location_id(1)

    return -zone.location_id(int(offset))
