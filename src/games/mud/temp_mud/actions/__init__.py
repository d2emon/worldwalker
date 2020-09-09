from .action import ActionList
from .bprintf import Log, Snoop
from .extra import Levels, Help, Value, Stats, Examine, Where, ListWizards, InCommand, Jump, Patch
from .frob import Frobnicate
from .magic import DeletePlayer, ChangePassword, Summon, GoToLocation, BecomeInvisible, BecomeVisible, Wizards, \
    Smoke, Ressurect
from .mobile import Crash, Sing, Spray, Directory
from .new1 import Wear, Remove, Put, Wave, Open, Close, Lock, Unlock, Force, Light, Extinguish, Push, Cripple, Cure, \
    Dumb, Change, Missile, Shock, Fireball, Blow, Sigh, Kiss, Hug, Slap, Tickle, Scream, Bounce, Stare, Grope, \
    Deaf, Squeeze, Cuddle, Blind
from .objsys import Take, Drop, Inventory, Who, Users
from .parse import Go, GoNorth, GoEast, GoSouth, GoWest, GoUp, GoDown, QuitWorld, Look, Reset, Lightning, Eat, Play, \
    Shout, Say, Tell, Save, Score, Exorcise, Give, Steal, Tss, RmEdit, USystem, INumber, Update, Become, SysStat, \
    Converse, Shell, Raw, Roll, Credits, Brief, Debug, MapWorld, Flee, Bug, Typo, Pronouns, DebugMode, SetIn, SetOut, \
    SetMin, SetMout, Dig, Empty
from .weather import Storm, Rain, Sun, Snow, Blizzard, Laugh, Cry, Burp, Fart, Hiccup, Grin, Smile, Wink, Snigger, \
    Pose, SetValue, Pray, Groan, Moan, Yawn, Purr, Sulk, SetPFlags, Emote
from .zones import Exits, Loc


# Parse
class VerbsList(ActionList):
    def __init__(self):
        super().__init__(
            Go,
            GoNorth,
            GoEast,
            GoSouth,
            GoWest,
            GoUp,
            GoDown,
            QuitWorld,
            Take,
            Drop,

            Look,
            Inventory,
            Who,
            Reset,
            Lightning,
            Eat,
            Play,
            Shout,
            Say,
            Tell,

            Save,
            Score,
            Exorcise,
            Give,
            Steal,
            Levels,
            Help,
            Value,
            Stats,
            Examine,

            DeletePlayer,
            ChangePassword,
            Summon,
            # 34
            # 35

            # ? 36-49

            Laugh,

            Cry,
            Burp,
            Fart,
            Hiccup,
            Grin,
            Smile,
            Wink,
            Snigger,
            Pose,
            SetValue,

            Pray,
            Storm,
            Rain,
            Sun,
            Snow,
            GoToLocation,

            # ? 67-99

            Wear,

            Remove,
            Put,
            Wave,
            Blizzard,
            Open,
            Close,
            Lock,
            Unlock,
            Force,
            Light,

            Extinguish,
            Where,
            # 113 -> 117
            BecomeInvisible,
            BecomeVisible,
            # - 116
            Push,
            Cripple,
            Cure,
            Dumb,

            Change,
            Missile,
            Shock,
            Fireball,
            # - 125
            Blow,
            Sigh,
            Kiss,
            Hug,
            Slap,

            Tickle,
            Scream,
            Bounce,
            Wizards,
            Stare,
            Exits,
            Crash,
            Sing,
            Grope,
            Spray,

            Groan,
            Moan,
            Directory,
            Yawn,
            ListWizards,
            InCommand,
            Smoke,
            Deaf,
            Ressurect,
            Log,

            Tss,
            RmEdit,
            Loc,
            Squeeze,
            Users,
            USystem,
            INumber,
            Update,
            Become,
            SysStat,

            Converse,
            Snoop,
            Shell,
            Raw,
            Purr,
            Cuddle,
            Sulk,
            Roll,
            Credits,
            Brief,

            Debug,
            Jump,
            MapWorld,
            Flee,
            Bug,
            Typo,
            Pronouns,
            Blind,
            Patch,
            DebugMode,

            SetPFlags,
            Frobnicate,
            SetIn,
            SetOut,
            SetMin,
            SetMout,
            Emote,
            Dig,
            Empty,
        )