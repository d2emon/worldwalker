from ..errors import CommandError, CrapupError
from ..blood import Blood
from ..mobile import dragget
from ..newuaf import NewUaf
from ..parse.messages import Message
from ..support import Item, Player, ohany, iscarrby
from ..tk import Tk, broad, loseme, trapch
from ..weather import sillycom
from . import teletrap, woundmn
from .disease import DISEASES
from .messages import MSG_GLOBAL, MSG_CURE, MSG_CRIPPLE, MSG_DUMB, MSG_FORCE, MSG_BOLT, MSG_BLIND, MSG_CHANGE, \
    MSG_FIREBALL, MSG_SHOCK, MSG_DEAF
from .utils import get_item, victim_is_here, victim_magic, victim_magic_is_here, social


