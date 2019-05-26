"""
Some more basic functions

Note

state(obj)
setstate(obj,val)
destroy(obj)

are elsewhere
"""
from services.world import WorldService


class Player:
    PLAYERS_COUNT = 48

    GENDER_IT = 0
    GENDER_HE = 1
    GENDER_SHE = 2

    players = []
    maxu = 16

    def __init__(self, player_id, name=None, curch=None):
        self.player_id = player_id
        self.name = name
        self.location = curch
        self.position = None
        self.level = 1
        self.visible = 0
        self.strength = -1
        self.weapon = None
        self.sex_all = 0
        self.helping = None

    @property
    def __data(self):
        # 0  Name
        # 1
        # 2
        # 3
        # 4  Location
        # 5  Position
        # 6
        # 7  Strength
        # 8  Visible
        # 9  Flags
        # 10 Level
        # 11 Weapon
        # 12
        # 13 Helping
        # 14
        # 15
        return WorldService.get_player(self.player_id)

    @property
    def name(self):
        return self.__data[0]

    @name.setter
    def name(self, value):
        self.__data[0] = value

    @property
    def location(self):
        return self.__data[4]

    @location.setter
    def location(self, value):
        self.__data[4] = value

    @property
    def channel(self):
        return self.__data[4]

    @property
    def position(self):
        return self.__data[5]

    @position.setter
    def position(self, value):
        self.__data[5] = value

    @property
    def strength(self):
        return self.__data[7]

    @strength.setter
    def strength(self, value):
        self.__data[7] = value

    @property
    def visible(self):
        return self.__data[8]

    @visible.setter
    def visible(self, value):
        self.__data[8] = value

    @property
    def sex_all(self):
        """
        Pflags

        0 sex
        1 May not be exorcised ok
        2 May change pflags ok
        3 May use rmedit ok
        4 May use debugmode ok
        5 May use patch
        6 May be snooped upon

        :return:
        """
        return self.__data[9]

    @sex_all.setter
    def sex_all(self, value):
        self.__data[9] = value

    @property
    def sex(self):
        return self.__data[9][0]

    @sex.setter
    def sex(self, value):
        self.__data[9][0] = value

    @property
    def level(self):
        return self.__data[10]

    @level.setter
    def level(self, value):
        self.__data[10] = value

    @property
    def weapon(self):
        return self.__data[11]

    @weapon.setter
    def weapon(self, value):
        self.__data[11] = value

    @property
    def helping(self):
        return self.__data[13]

    @helping.setter
    def helping(self, value):
        self.__data[13] = value

    @property
    def exists(self):
        return self.name is not None

    @property
    def gender(self):
        """

        :return:
        """
        riatha = self.fpbns('riatha')
        shazareth = self.fpbns('shazareth')
        if self.player_id > 15 and self not in [riatha, shazareth]:
            return self.GENDER_IT
        elif self.sex:
            return self.GENDER_SHE
        else:
            return self.GENDER_HE

    def remove(self):
        self.name = None

    @classmethod
    def fill(cls):
        cls.players = [cls(player_id) for player_id in range(cls.PLAYERS_COUNT)]

    @classmethod
    def find_empty(cls):
        for player_id, player in enumerate(cls.players):
            if not player.exists:
                return player_id
        raise OverflowError()

    def add(self):
        self.players[self.player_id] = self

    @classmethod
    def put_on(cls, name, channel):
        player_id = cls.find_empty()
        cls(player_id, name, channel).add()
        return player_id

    @classmethod
    def fpbns(cls, name):
        search = name.lower()
        for player in cls.players:
            if not player.exists:
                continue
            player_name = player.name.lower()
            if player_name == search:
                return player
            if player_name[:4] == "the ":
                if player_name[4:] == search:
                    return player
        return None



"""
ptothlp(pl)
{
int tot;
extern long maxu;
int ct=0;
while(ct<maxu)
{
if(ploc(ct)!=ploc(pl)){ct++;continue;}
if(phelping(ct)!=pl){ct++;continue;}
return(ct);
}
return(-1);
}
 

psetflg(ch,x)
long ch;
long x;
{
	extern long ublock[];
	ublock[16*ch+9]|=(1<<x);
}

pclrflg(ch,x)
long ch;
long x;
{
	extern long ublock[];
	ublock[16*ch+9]&=~(1<<x);
}



ptstbit(ch,x)
long ch;
long x;
{
	return(ptstflg(ch,x));
}


ptstflg(ch,x)
long ch;
long x;
{
	extern long ublock[];
	extern char globme[];
	if((x==2)&&(strcmp(globme,"Debugger")==0)) return(1<<x);
	return(ublock[16*ch+9]&(1<<x));
}
"""



"""
#include "object.h"
#include <stdio.h>
#include "files.h"

extern FILE* openlock();
 /*


 */
extern OBJECT objects[];

 ocarrf(ob)
    {
    extern long objinfo[];
    return(objinfo[4*ob+3]);
    }

 setocarrf(ob,v)
    {
    extern long objinfo[];
    objinfo[4*ob+3]=v;
    }

 oloc(ob)
    {
    extern long objinfo[];
    return(objinfo[4*ob]);
    }

 setoloc(ob,l,c)
    {
    extern long objinfo[];
    objinfo[4*ob]=l;
    objinfo[4*ob+3]=c;
    }



char * oname(ob)
    {
    extern OBJECT objects[];
    return(objects[ob].o_name);
    }
 
char * olongt(ob,st)
{
	extern OBJECT objects[];
	return(objects[ob].o_desc[st]);
}


 omaxstate(ob)
    {
    extern OBJECT objects[];
    return(objects[ob].o_maxstate);
    }

 obflannel(ob)  /* Old version */
    {
    return(oflannel(ob));
    }
 oflannel(ob)
    {
    extern OBJECT objects[];
    return(objects[ob].o_flannel);
    }

 obaseval(ob)
    {
    extern OBJECT objects[];
    return(objects[ob].o_value);
    }

 isdest(ob)
    {
    if(otstbit(ob,0))return(1);
    return(0);
    }

 isavl(ob)
    {
    extern long mynum;
    if(ishere(ob)) return(1);
    return(iscarrby(ob,mynum));
    }

 ospare(ob)
    {
    return(otstbit(ob,0)?-1:0);
    }

ocreate(ob)
{
oclrbit(ob,0);
}

syslog(args,arg1,arg2)
char *args,*arg1,*arg2;
{
extern char *strchr();	
extern char *ctime();
long tm;
FILE *x;
char *z;
time(&tm);
z=ctime(&tm);
*strchr(z,'\n')=0;
x=openlock(LOG_FILE,"a");
if(x==NULL) {loseme();crapup("Log fault : Access Failure"); }
fprintf(x,"%s:  ",z);
fprintf(x,args,arg1,arg2);
fprintf(x,"\n");
fclose(x);
}
 
osetbit(ob,x)
{
extern long objinfo[];
bit_set(&(objinfo[4*ob+2]),x);
}
oclearbit(ob,x)
{
extern long objinfo[];
bit_clear(&(objinfo[4*ob+2]),x);
}
oclrbit(ob,x)
{
oclearbit(ob,x)
;
}
otstbit(ob,x)
{
extern long objinfo[];
return(bit_fetch(objinfo[4*ob+2],x));
}
osetbyte(o,x,y)
{
extern long objinfo[];
byte_put(&(objinfo[4*o+2]),x,y);
}
obyte(o,x)
{
extern long objinfo[];
return(byte_fetch(objinfo[4*o+2],x));
}
ohany(mask)
long mask;
{
extern long numobs;
auto a;
extern long mynum;
extern long objinfo[];
a=0;
mask=mask<<16;
while(a<numobs)
{
if(((iscarrby(a,mynum))||(ishere(a,mynum)))&&(objinfo[4*a+2]&mask))return(1);
a++;
}
return(0);
}

"""
