from .action import ActionList
from .parse import Go, GoNorth, GoEast, GoSouth, GoWest, GoUp, GoDown, QuitWorld, Reset, Lightning, Eat, Play, Grope, \
    Credits, Brief, MapWorld, Flee, DebugMode
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
            # 9
            # 10

            # 11
            # 12
            # 13
            Reset,
            Lightning,
            Eat,
            Play,
            # 18
            # 19
            # 20

            # 21
            # 22
            # 23
            # 24
            # 25
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

            # 151
            # 152
            Loc,
            # 154
            # 155
            # 156
            # 157
            # 158
            # 159
            # 160

            # 161
            # 162
            # 163
            # 164
            Purr,
            # 166
            Sulk,
            # 168
            Credits,
            Brief,

            # 171
            # 172
            MapWorld,
            Flee,
            # 175
            # 176
            # 177
            # 178
            # 179
            DebugMode,

            SetPFlags,
            # 182
            # 183
            # 184
            # 185
            # 186
            Emote,
            # 188
            # 189
        )
