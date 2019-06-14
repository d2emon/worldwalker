from .action import ActionList
from .objsys import Take, Inventory
from .parse import Go, GoNorth, GoEast, GoSouth, GoWest, GoUp, GoDown, QuitWorld, Look, Reset, Lightning, Eat, Play, \
    Shout, Say, Tell, Score, Exorcise, Give, Steal, Grope, Tss, RmEdit, USystem, INumber, Update, Become, SysStat, \
    Converse, Shell, Raw, Roll, Credits, Brief, Debug, MapWorld, Flee, Bug, Typo, DebugMode, SetIn, SetOut, SetMin, \
    SetMout, Dig, Empty
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
            # 10

            Look,
            Inventory,
            # 13
            Reset,
            Lightning,
            Eat,
            Play,
            Shout,
            Say,
            Tell,

            # 21
            Score,
            Exorcise,
            Give,
            Steal,
            # 26
            # 27
            # 28
            # 29
            # 30

            # 31
            # 32
            # 33
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
            # 66

            # ? 67-99

            # 100

            # 101
            # 102
            # 103
            Blizzard,
            # 105
            # 106
            # 107
            # 108
            # 109
            # 110

            # 111
            # - 112
            # 113
            # - 114
            # - 115
            # - 116
            # 117
            # 118
            # 119
            # 110

            # 121
            # 122
            # 123
            # 124
            # 125
            # 126
            # 127
            # 128
            # 129
            # 130

            # 131
            # 132
            # 133
            # 134
            # 135
            Exits,
            # 137
            # 138
            Grope,
            # 140

            Groan,
            Moan,
            # 143
            Yawn,
            # 145
            # 146
            # 147
            # 148
            # 149
            # 150

            Tss,
            RmEdit,
            Loc,
            # 154
            # 155
            USystem,
            INumber,
            Update,
            Become,
            SysStat,

            Converse,
            # 162
            Shell,
            Raw,
            Purr,
            # 166
            Sulk,
            Roll,
            Credits,
            Brief,

            Debug,
            # 172
            MapWorld,
            Flee,
            Bug,
            Typo,
            # 177
            # 178
            # 179
            DebugMode,

            SetPFlags,
            SetIn,
            SetOut,
            SetMin,
            SetMout,
            # 186
            Emote,
            Dig,
            Empty,
        )
