from .action import ActionList
from .parse import Go, GoNorth, GoEast, GoSouth, GoWest, GoUp, GoDown, QuitWorld, Groan, Credits, Brief, MapWorld, \
    Flee, DebugMode


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
            # 14
            # 15
            # 16
            # 17
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

            # 50

            # 51
            # 52
            # 53
            # 54
            # 55
            # 56
            # 57
            # 58
            # 59
            # 60

            # 161
            # 162
            # 163
            # 164
            # 165
            # 166

            # 100

            # 101
            # 102
            # 103
            # 104
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
            # 136
            # 137
            # 138
            # 139
            # 130

            # 141
            # 142
            # 143
            # 144
            # 145
            # 146
            # 147
            # 148
            # 149
            # 150

            # 151
            # 152
            # 153
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
            # 165
            # 166
            # 167
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
        )
