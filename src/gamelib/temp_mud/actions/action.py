from gamelib.temp_mud.errors import CommandError
from gamelib.temp_mud.world import World


"""
"go","climb",
"n","e","s","w","u","d",
"north","east","south","west","up","down",
"quit","get","take","drop",
"look","i","inv","inventory","who","reset","zap","eat","drink","play","shout","say","tell",
"save","score","exorcise","give","steal","pinch","levels","help","value","stats","examine","read",
"delete","pass","password","summon","weapon","wield","shoot","kill","hit","fire","launch","smash","break","strike",
"laugh",
"cry","burp","fart","hiccup","grin","smile","wink","snigger","pose","set",
"pray","storm","rain","sun","snow","goto",
"wear",

"remove","put","wave","blizzard","open","close","shut","lock","unlock","force","light",
"extinguish","where","invisible","visible","turn","pull","press","push","cripple","cure","dumb",
"change","missile","shock","fireball","translocate","blow","sigh","kiss","hug","slap",
"tickle","scream","bounce","wiz","stare","exits","crash","sing","grope","spray",
"groan","moan","directory","yawn","wizlist","in","smoke","deafen","resurrect","log",
"tss","rmedit","loc","squeeze","users","honeyboard","inumber","update","become","systat",
"converse","snoop","shell","raw","purr","cuddle","sulk","roll","credits","brief",
"debug","jump","map","flee","bug","typo","pn","blind","patch","debugmode",
"pflags","frobnicate","setin","setout","setmin","setmout","emote","dig","empty"

1,1,
2,3,4,5,6,7,
2,3,4,5,6,7,
8,9,9,10,
11,12,12,12,13,14,15,16,16,17,18,19,20,
21,22,23,24,25,25,26,27,28,29,30,30,
31,32,32,33,34,34,35,35,35,35,35,35,35,35,
50,
51,52,53,54,55,56,57,58,59,60,
61,62,63,64,65,66,
100,

101,102,103,104,105,106,106,107,108,109,110,
111,112,114,115,117,117,117,117,118,119,120,
121,122,123,124,125,126,127,128,129,130,
131,132,133,134,135,136,137,138,139,140,
141,142,143,144,145,146,147,148,149,150,
151,152,153,154,155,156,157,158,159,160,
161,162,163,164,165,166,167,168,169,170,
171,172,173,174,175,176,177,178,179,180,
181,182,183,184,185,186,187,188,189


case 1:
case 8:
case 9:
case 10:

case 11:
case 12:
case 13:
case 14:
case 15:
case 16:
case 17:
case 18:
case 19:
case 20:

case 21:
case 22:
case 23:
case 24:
case 25:
       case 26:
          levcom();
          break;
       case 27:
          helpcom();
          break;
       case 28:
          valuecom();
          break;
       case 29:
          stacom();
          break;
       case 30:
          examcom();
          break;

case 31:
          delcom();
          break;
       case 32:
          passcom();
          break;
       case 33:
          sumcom();
          break;
       case 34:
          weapcom();
          break;
       case 35:
          killcom();
          break;

case 50:

case 51:
case 52:
case 53:
case 54:
case 55:
case 56:
case 57:
case 58:
case 59:
case 60:

case 61:
case 62:
case 63:
case 64:
case 65:
       case 66:
          goloccom();
          break;

case 100:

case 101:
case 102:
case 103:
case 104:
case 105:
case 106:
case 107:
case 108:
case 109:
case 110:

case 111:
case 113:
case 117: case 113;
case 118:
case 119:
case 120:

case 121:
case 122:
case 123:
case 124:
case 126:
case 127:
case 128:
case 129:
case 130:

case 131:
case 132:
case 133:
       case 134:
          wizcom();
          break;
case 135:
case 136:
case 137:
case 138:
case 139:
case 140:

case 141:
case 142:
       case 143:
          dircom();
          break;
case 144:
       case 145:
          wizlist();
          break;
       case 146:
          incom();
          break;
       case 147:
          lightcom();
          break;
       case 114:
          inviscom();
          break;
       case 115:
          viscom();
          break;
case 148:
       case 149:
          ressurcom();
          break;
       case 150:
          logcom();
          break;

case 151:
case 152:
case 154:
case 153:
case 155:
case 156:
case 157:
case 158:
case 159:
case 160:

case 161:
       case 162:
          snoopcom();
          break;
case 163:
case 164:
case 165:
case 166:
case 167:
case 168:
case 169:
case 170:

case 171:
       case 172:
          jumpcom();
          break;
       case 112:
          wherecom();
          break;
case 173:
case 174:
case 175:
case 176:
case 177:
case 178:
       case 179:
          edit_world();
          break;
case 180:

case 181:
       case 182:
          frobnicate();
          break;
case 183:
case 184:
case 185:
case 186:
case 187:
case 188:
case 189:
default:
"""


# Parse
class BaseAction:
    WEIGHTS = {
        0: 3,
        1: 2,
    }
    full_match = False
    commands = "",

    @classmethod
    def match(cls, word):
        if not word:
            return 0
        if word in cls.commands:
            return 10000
        if cls.full_match:
            return -1
        values = []
        for command in cls.commands:
            values.append(sum((cls.WEIGHTS.get(i, 1) for i, c in enumerate(word[:len(command)]) if c == command[i])))
        return max(values)

    @classmethod
    def prepare(cls, command, parser):
        return command

    @classmethod
    def validate(cls, command, parser):
        return True

    @classmethod
    def action(cls, command, parser):
        raise NotImplementedError("I don't know that verb\n")

    @classmethod
    def execute(cls, command, parser):
        World.load()
        cls.validate(command, parser)
        return cls.action(command, parser)


# Unknown
class Action(BaseAction):
    wizard_only = None
    god_only = None

    @classmethod
    def action(cls, command, parser):
        if parser.user.is_god:
            raise NotImplementedError("Sorry not written yet[COMREF {}]\n".format(command))
        raise NotImplementedError("I don't know that verb.\n")

    @classmethod
    def prepare(cls, parser, action):
        if action == ".q":
            return ""  # Otherwise drops out after command
        elif not action:
            return ""
        elif action == "!":
            return parser.string_buffer
        return action

    @classmethod
    def validate(cls, command, parser):
        if cls.god_only and not parser.user.is_god:
            raise CommandError(cls.god_only)
        if cls.wizard_only and not parser.user.is_wizard:
            raise CommandError(cls.wizard_only)
        return True


class Spell(Action):
    reflect = False

    @classmethod
    def cast(cls, parser, target):
        raise NotImplementedError()

    @classmethod
    def action(cls, command, parser):
        target = parser.get_target(False)

        if parser.user.strength < 10:
            raise CommandError("You are too weak to cast magic\n")

        spell_level = 5
        if Item(111).is_carried_by(parser.user):
            spell_level += 1
        if Item(121).is_carried_by(parser.user):
            spell_level += 1
        if Item(163).is_carried_by(parser.user):
            spell_level += 1

        if not parser.user.is_wizard:
            parser.user.strength -= 2
            if randperc() > spell_level * parser.user.level:
                yield ("You fumble the magic\n")
                if not cls.reflect:
                    raise CommandError()
                yield ("The spell reflects back\n")
                target = parser.user
            else:
                yield ("The spell succeeds!!\n")

        if cls.reflect and target.location.location_id != parser.user.location_id:
            raise CommandError("They are not here\n")

        yield from cls.cast(parser, target)


class Special(BaseAction):
    @classmethod
    def action(cls, command, parser):
        raise NotImplementedError("\nUnknown . option\n")

    @classmethod
    def prepare(cls, parser, action):
        if not action:
            return
        if action[0] != ".":
            return
        return action[1:].lower()


class ActionList:
    default_action = Action

    def __init__(self, *items):
        self.items = items

    def check(self, word):
        best_value = 0
        best_item = self.default_action

        word = word.lower()
        values = (item.match(word), item for item in self.items if item.match(word) < 5)
        for value, item in values:
            if value <= best_value:
                continue
            best_value = value
            best_item = item
        return best_item
