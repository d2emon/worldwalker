"""
The next part of the universe...
"""

"""
Weather Routines
 
Current weather defined by state of object 47
 
states are
 
0   Sunny
1   Rain
2   Stormy
3   Snowing
"""


MSG_GLOBAL = -10000
MSG_WEATHER = -10030

WEATHER_SUN = 0
WEATHER_RAIN = 1
WEATHER_STORM = 2
WEATHER_SNOW = 3
WEATHER_BLIZZARD = 4

WEATHER_START = {
    WEATHER_SUN: "\001cThe sun comes out of the clouds\n\001",
    WEATHER_RAIN: "\001cIt has started to rain\n\001",
    WEATHER_SNOW: "\001cIt has started to snow\n\001",
    WEATHER_BLIZZARD: "\001cYou are half blinded by drifting snow, as a white, icy blizzard sweeps across\nthe "
                      "land\n\001",
}

WEATHER_TEXT = {
    WEATHER_STORM: "\001cThe skies are dark and stormy\n\001",
    WEATHER_SNOW: "\001cIt is snowing\001\n",
    WEATHER_BLIZZARD: "\001cA blizzard is howling around you\001\n",
}


class User:
    def __init__(self):
        self.has_farted = False
        self.channel_id = 0

    @property
    def location(self):
        return Location(self.channel_id)


class Location:
    def __init__(self, location_id):
        self.location_id = location_id

    @property
    def outdoors(self):
        if self.location_id in [-100, -101, -102]:
            return True
        elif self.location_id in [-170, -183]:
            return True
        elif -168 > self.location_id > -191:
            return True
        elif -181 > self.location_id > -172:
            return True
        else:
            return False


class __Weather:
    weather_id = None

    @classmethod
    def action(cls, user):
        if not user.is_wizard:
            raise Exception("What ?\n")
        adjust_weather(user, cls.weather_id)


class Sun(__Weather):
    weather_id = WEATHER_SUN


class Rain(__Weather):
    weather_id = WEATHER_RAIN


class Storm(__Weather):
    weather_id = WEATHER_STORM


class Snow(__Weather):
    weather_id = WEATHER_SNOW


class Blizzard(__Weather):
    weather_id = WEATHER_BLIZZARD


def adjust_weather(user, new_weather):
    weather = Item(0)
    old_weather = weather.state
    if new_weather != old_weather:
        weather.state = new_weather
        Message(
            user,
            user,
            MSG_WEATHER,
            new_weather,
        ).send()


def longwthr(user):
    chance = randperc()
    if chance < 50:
        return adjust_weather(user, 1)
    elif chance > 90:
        return adjust_weather(user, 2)
    else:
        return adjust_weather(user, 0)


def weather_receive(user, weather_id):
    if not user.location.outdoors():
        return
    weather_id = modifwthr(weather_id)
    yield WEATHER_START.get(weather_id, "")


def show_weather(user, weather_id):
    if not user.location.outdoors():
        return
    weather_id = modifwthr(weather_id)
    if weather_id == WEATHER_RAIN:
        if -178 > user.channel_id > -199:
            yield "It is raining, a gentle mist of rain, which sticks to everything around\n"
            yield "you making it glisten and shine. High in the skies above you is a rainbow\n"
        else:
            yield "\001cIt is raining\n\001"
        return
    yield WEATHER_TEXT.get(weather_id, "")


# Silly Section

class Silly:
    not_dumb = False
    message = ""
    result = ""

    @classmethod
    def action(cls, user):
        if cls.not_dumb:
            user.diseases.dumb.check()
        Message(
            user,
            user,
            MSG_GLOBAL,
            user.channel_id,
            cls.message.format(user=user),
        )
        yield cls.result


class Laugh(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d falls over laughing\n\001"
    result = "You start to laugh\n"


class Purr(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d starts purring\n\001"
    result = "MMMMEMEEEEEEEOOOOOOOWWWWWWW!!\n"


class Cry(Silly):
    not_dumb = True
    message = "\001s{user.name}\001{user.name} bursts into tears\n\001"
    result = "You burst into tears\n"


class Sulk(Silly):
    message = "\001s{user.name}\001{user.name} sulks\n\001"
    result = "You sulk....\n"


class Burp(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d burps loudly\n\001"
    result = "You burp rudely\n"


class Hiccup(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d hiccups\n\001"
    result = "You hiccup\n"


class Fart(Silly):
    message = "\001P{user.name}\001\001d lets off a real rip roarer\n\001"
    result = "Fine...\n"

    @classmethod
    def action(cls, user):
        user.has_farted = True
        super().action(user)


class Grin(Silly):
    message = "\001s{user.name}\001{user.name} grins evilly\n\001"
    result = "You grin evilly\n"


class Smile(Silly):
    message = "\001s{user.name}\001{user.name} smiles happily\n\001"
    result = "You smile happily\n"


class Wink(Silly):
    # At person later maybe ?
    message = "\001s{user.name}\001{user.name} winks suggestively\n\001"
    result = "You wink\n"


class Snigger(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d sniggers\n\001"
    result = "You snigger\n"


"""
 posecom()
    {
    long a;
    extern long my_lev;
    if(my_lev<10)
       {
       bprintf("You are just not up to this yet\n");
       return;
       }
    time(&a);
    srand(a);
    a=randperc();
    a=a%5;
    bprintf("POSE :%d\n",a);
    switch(a)
       {
       case 0:
          break;
       case 1:
	sillycom("\001s%s\001%s throws out one arm and sends a huge bolt of fire high\n\
into the sky\n\001");
          broad("\001cA massive ball of fire explodes high up in the sky\n\001");
          break;
       case 2:
          sillycom("\001s%s\001%s turns casually into a hamster before resuming normal shape\n\001");
          break;
       case 3:
          sillycom("\001s%s\001%s \
starts sizzling with magical energy\n\001");
          break;
       case 4:
          sillycom("\001s%s\001%s begins to crackle with magical fire\n\001");
          break;
          }
    }

 emotecom()
 /*
  (C) Jim Finnis
 */
 {
 	extern long my_lev;
 	char buf[100];
 	strcpy(buf,"\001P%s\001 ");
 	getreinput(buf+6);
 	strcat(buf,"\n");
 	if (my_lev<10000)
 		bprintf("Your emotions are strictly limited!\n");
	else
		sillycom(buf);
}
		
 praycom()
    {
    extern long curch;
    sillycom("\001s%s\001%s falls down and grovels in the dirt\n\001");
    bprintf("Ok\n");
    }

 yawncom()
    {
    sillycom("\001P%s\001\001d yawns\n\001");
    }
 
 groancom()
    {
    sillycom("\001P%s\001\001d groans loudly\n\001");
    bprintf("You groan\n");
    }
 
 moancom()
    {
    sillycom("\001P%s\001\001d starts making moaning noises\n\001");
    bprintf("You start to moan\n");
    }
 
 cancarry(plyr)
    {
    extern long numobs;
    long a,b;
    a=0;
    b=0;
    if(plev(plyr)>9) return(1);
    if(plev(plyr)<0) return(1);
    while(a<numobs)
       {
       if((iscarrby(a,plyr))&&(!isdest(a))) b++;
       a++;
       }
    if(b<plev(plyr)+5) return(1);
    return(0);
    }
 
 
 setcom()
    {
    long a,b,c;
    extern long my_lev;
    extern char wordbuf[];
    if(brkword()== -1)
       {
       bprintf("set what\n");
       return;
       }
    if(my_lev<10)
       {
       bprintf("Sorry, wizards only\n");
       return;
       }
    a=fobna(wordbuf);
    if(a== -1)
       {
         goto setmobile;
       }
    if(brkword()== -1)
       {
       bprintf("Set to what value ?\n");
       return;
       }
       if(strcmp(wordbuf,"bit")==0) goto bitset;
       if(strcmp(wordbuf,"byte")==0) goto byteset;
    b=numarg(wordbuf);
    if(b>omaxstate(a))
       {
       bprintf("Sorry max state for that is %d\n",omaxstate(a));
       return;
       }
    if(b<0)
       {
       bprintf("States start at 0\n");
       return;
       }
    setstate(a,b);
    return;
bitset:if(brkword()==-1)
       {
       	   bprintf("Which bit ?\n");
       	   return;
       	}
       	b=numarg(wordbuf);
       	if(brkword()==-1)
       	{
       	   bprintf("The bit is %s\n",otstbit(a,b)?"TRUE":"FALSE");
       	   return;
       	}
       	c=numarg(wordbuf);
       	if((c<0)||(c>1)||(b<0)||(b>15))
       	{
       		bprintf("Number out of range\n");
       		return;
       	}
       	if(c==0) oclrbit(a,b);
       	else osetbit(a,b);
       	return;
byteset:if(brkword()==-1)
       {
       	   bprintf("Which byte ?\n");
       	   return;
       	}
       	b=numarg(wordbuf);
       	if(brkword()==-1)
       	{
       	   bprintf("Current Value is : %d\n",obyte(a,b));
       	   return;
       	}
       	c=numarg(wordbuf);
       	if((b<0)||(b>1)||(c<0)||(c>255))
       	{
       		bprintf("Number out of range\n");
       		return;
       	}
	osetbyte(a,b,c);
       	return;       
setmobile:a=fpbn(wordbuf);
           if(a==-1)
           {
           	bprintf("Set what ?\n");
           	return;
           }
           if(a<16)
           {
           	bprintf("Mobiles only\n");
           	return;
           }
           if(brkword()==-1)
           {
           	bprintf("To what value ?\n");
           	return;
           }
           b=numarg(wordbuf);
           setpstr(a,b);
    }
 
 
 
isdark()
    {
long c;
extern long curch,my_lev;
extern long numobs;
if(my_lev>9) return(0);
if((curch==-1100)||(curch==-1101)) return(0);
if((curch<=-1113)&&(curch>=-1123)) goto idk;
if((curch<-399)||(curch>-300)) return(0);
idk:c=0;
while(c<numobs)
{
if((c!=32)&&(otstbit(c,13)==0)) {c++;continue;}
if(ishere(c)) return(0);
if((ocarrf(c)==0)||(ocarrf(c)==3)) {c++;continue;}
if(ploc(oloc(c))!=curch) {c++;continue;}
return(0);
}
return(1);
}
 
 
 
modifwthr(n)
{
extern long curch;
switch(curch)
{
default:
if((curch>=-179)&&(curch<=-199)) 
{
	if(n>1)return(n%2);
	else return(n);
}
if((curch>=-178)&&(curch<=-100))
{
	if((n==1)||(n==2)) n+=2;
	return(n);
}
return(n);
}
}

setpflags()
{
	long a,b,c,d;
	extern long mynum;
	extern char wordbuf[];
	if(!ptstbit(mynum,2))
	{
		bprintf("You can't do that\n");
		return;
	}
	if(brkword()==-1) 
	{
		bprintf("Whose PFlags ?\n");
		return;
	}
	a=fpbn(wordbuf);
	if(a==-1)
	{
		bprintf("Who is that ?\n");
		return;
	}
	if(brkword()==-1)
	{
		bprintf("Flag number ?\n");
		return;
	}
	b=numarg(wordbuf);
	if(brkword()==-1)
	{
		bprintf("Value is %s\n",ptstflg(a,b)?"TRUE":"FALSE");
		return;
	}
	c=numarg(wordbuf);
	if((c<0)||(c>1)||(b<0)||(b>31))
	{
		bprintf("Out of range\n");
		return;
	}
	if(c) psetflg(a,b);
	else pclrflg(a,b);
}
"""
