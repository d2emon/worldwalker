"""
Some more basic functions

Note

state(obj)
setstate(obj,val)
destroy(obj)

are elsewhere
"""
from services.world import WorldService
from services.world.player import PlayerServices


class Player:
    def __init__(self, player_id, name=None, channel=None):
        self.player_id = player_id
        self.__data = {
            'name': name,
            'location': channel,
            'position': None,
            'level': 1,
            'visible': 0,
            'strength': -1,
            'weapon': None,
            'sex': [0] * 8,
            'helping': None,
        }
        self.save()

    @property
    def name(self):
        return self.__data.get('name')

    @name.setter
    def name(self, value):
        self.__data['name'] = value
        self.save()

    @property
    def location(self):
        return self.__data.get('location')

    @location.setter
    def location(self, value):
        self.__data['location'] = value
        self.save()

    @property
    def position(self):
        return self.__data.get('position', None)

    @position.setter
    def position(self, value):
        self.__data['position'] = value
        self.save()

    @property
    def level(self):
        return self.__data.get('level', 1)

    @level.setter
    def level(self, value):
        self.__data['level'] = value
        self.save()

    @property
    def visible(self):
        return self.__data.get('visible', 0)

    @visible.setter
    def visible(self, value):
        self.__data['visible'] = value
        self.save()

    @property
    def strength(self):
        return self.__data.get('strength', -1)

    @strength.setter
    def strength(self, value):
        self.__data['strength'] = value
        self.save()

    @property
    def weapon(self):
        return self.__data.get('weapon', None)

    @weapon.setter
    def weapon(self, value):
        self.__data['weapon'] = value
        self.save()

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
        return self.__data.get('sex')

    @sex_all.setter
    def sex_all(self, value):
        self.__data['sex'] = value
        self.save()

    @property
    def sex(self):
        return self.__data.get('sex', [])[0]

    @sex.setter
    def sex(self, value):
        self.__data.get('sex', [])[0] = value
        self.save()

    @property
    def helping(self):
        return self.__data.get('helping')

    @helping.setter
    def helping(self, value):
        self.__data['helping'] = value
        self.save()

    @property
    def exists(self):
        return self.name is not None

    def remove(self):
        self.name = None

    def load(self):
        self.__data = PlayerServices.get_player(self.player_id)
        return self

    def save(self):
        PlayerServices.put_player(self.player_id, self.__data)
        return True

    def start(self, uaf):
        self.__data.update({
            'strength': uaf.strength,
            'level': uaf.level,
            'visible': 0 if uaf.level < 10000 else 10000,
            'weapon': None,
            'sex': uaf.sex,
            'helping': None,
        })
        return self.save()

    @property
    def data(self):
        return self.__data

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
