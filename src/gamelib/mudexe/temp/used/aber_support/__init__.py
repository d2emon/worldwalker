"""
Some more basic functions

Note

state(obj)
setstate(obj,val)
destroy(obj)

are elsewhere
"""
from gamelib.mudexe.temp.database.models.object import MudObject
from gamelib.mudexe.temp.database import Person


def syslog(*args):
    tm = time()
    z = ctime(tm).replace("\n", "")
    x = openlock(LOG_FILE, "a")
    if x is None:
        loseme()
        crapup("Log fault : Access Failure")
    x.write("{}:  ".format(z))
    x.write(args)
    x.write("\n")
    x.close()


# Objects
def oname(object_id):
    return objects[object_id].o_name


def olongt(object_id, state):
    return objects[object_id].o_desc[state]


def omaxstate(object_id):
    return objects[object_id].o_maxstate


def obflannel(object_id):
    # Old version
    return oflannel(object_id)


def oflannel(object_id):
    return objects[object_id].o_flannel


def obaseval(object_id):
    return objects[object_id].o_value


# Objects Data
def oloc(object_id):
    return MudObject.items[4 * object_id]


def setoloc(object_id, value):
    MudObject.items[4 * object_id] = value


def ocarrf(object_id):
    return MudObject.items[4 * object_id + 3]


def setocarrf(object_id, value):
    MudObject.items[4 * object_id + 3] = value


# Object Bits
def osetbit(object_id, x):
    bit_set(MudObject.items[4 * object_id + 2], x)


def oclearbit(object_id, x):
    bit_clear(MudObject.items[4 * object_id + 2], x)


def otstbit(object_id, x):
    return bit_fetch(MudObject.items[4 * object_id + 2], x)


def osetbyte(object_id, x, y):
    return byte_put(MudObject.items[4 * object_id + 2], x, y)


def obyte(object_id, x):
    return byte_fetch(MudObject.items[4 * object_id + 2], x)


def isdest(object_id):
    if otstbit(object_id, 0):
        return 1
    return 0


def isavl(object_id):
    if ishere(object_id):
        return 1
    return iscarrby(object_id, user.person_id)


def ospare(object_id):
    if otstbit(object_id, 0):
        return None
    return 0


def ocreate(object_id):
    oclrbit(object_id, 0)


def oclrbit(object_id, x):
    oclearbit(object_id, x)


def ohany(mask):
    a = 0
    mask = mask << 16
    for a in range(numobs):
        if iscarrby(a, user.person_id) or ishere(a, user.person_id) and MudObject.items[4 * a + 2] and mask:
            return True
    return False


# Persons
def pname(person_id):
    return Person.items[16 * person_id]


def pchan(person_id):
    return Person.items[16 * person_id + 4]


def ploc(person_id):
    return Person.items[16 * person_id + 4]


def setploc(person_id, value):
    Person.items[16 * person_id + 5] = value


def ppos(person_id):
    return Person.items[16 * person_id + 5]


def setppos(person_id, value):
    Person.items[16 * person_id + 5] = value


def pstr(person_id):
    return Person.items[16 * person_id + 7]


def setpstr(person_id, value):
    print(person_id, value)
    print(Person.items)
    Person.items[16 * person_id + 7] = value


def pvis(person_id):
    return Person.items[16 * person_id + 8]


def setpvis(person_id, value):
    Person.items[16 * person_id + 8] = value


def psexall(person_id):
    return Person.items[16 * person_id + 9]


def setpsexall(person_id, value):
    Person.items[16 * person_id + 9][0] = value


def psex(person_id):
    return Person.items[16 * person_id + 9][0]


def setpsex(person_id, value):
    Person.items[16 * person_id + 9] = value


def plev(person_id):
    return Person.items[16 * person_id + 10]


def setplev(person_id, value):
    Person.items[16 * person_id + 10] = value


def pwpn(person_id):
    return Person.items[16 * person_id + 11]


def setpwpn(person_id, value):
    Person.items[16 * person_id + 11] = value


def phelping(person_id):
    return Person.items[16 * person_id + 13]


def setphelping(person_id, value):
    Person.items[16 * person_id + 13] = value


# Person Bits
"""
Pflags

0 sex
1 May not be exorcised ok
2 May change pflags ok
3 May use rmedit ok
4 May use debugmode ok
5 May use patch 
6 May be snooped upon
"""
def psetflg(person_id, x):
    Person.items[16 * person_id + 9] = Person.items[16 * person_id + 9] or (1 << x)


def pclrflg(person_id, x):
    Person.items[16 * person_id + 9] = Person.items[16 * person_id + 9] and (1 << x)


def ptothlp(person_id):
    for ct in range(maxu):
        if ploc(ct) != ploc(person_id):
            continue
        if phelping(ct) != person_id:
            continue
        return ct
    return None


def ptstbit(person_id, x):
    return ptstflg(person_id, x)


def ptstflg(person_id, x):
    if x == 2 and user.name == "Debugger":
        return 1 << x
    return Person.items[16 * person_id + 9] and (1 << x)
