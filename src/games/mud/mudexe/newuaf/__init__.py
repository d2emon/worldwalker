from services.errors import FileServiceError, CrapupError
from services.file_services.person import Uaf


class Person:
    def __init__(self, name=None, score=0, strength=40, sex=None, level=1):
        self.name = name
        self.score = score
        self.strength = strength
        self.sex = sex
        self.level = level

    @classmethod
    def find(cls, name):
        data = Uaf.find(name)
        if data is None:
            return None
        return cls(**data)

    def save(self, name):
        Uaf.save(name, self)

    def decpers(self):
        return self.name, self.strength, self.score, self.level, self.sex

"""
delpers(name)
char *name;
{
	FILE *i;
	PERSONA x;
l1:	i=(FILE *)personactl(name,&x,PCTL_FIND);
	if(i==(FILE *)-1) return;
	lowercase(name);
	lowercase(x.p_name);
	if(strcmp(x.p_name,name))
	       crapup("Panic: Invalid Persona Delete");
	strcpy(x.p_name,"");
	x.p_level= -1;
	fwrite(&x,sizeof(PERSONA),1,i);
	fcloselock(i);
	goto l1;
}
"""

def initme(user):
    def moan1(person):
        user.output("\nSex (M/F) : ")
        user.show_buffer()
        keysetback()
        sex = getkbd(2).lower()
        keysetup()
        if sex == 'm':
            person.sex = 0
        elif sex == 'f':
            person.sex = 1
        else:
            user.output("M or F")
            return moan1(person)
        person.save(user.name)
        return person

    try:
        person = Person.find(user.name)
        if person is not None:
            return person
    except FileServiceError:
        raise CrapupError("Panic: Timeout event on user file\n")

    user.output("Creating character....\n")
    return moan1(Person(name=user.name))


"""
saveme()
{
	extern char globme[];
	extern long zapped;
	PERSONA x;
	extern int mynum;
	strcpy(x.p_name,globme);
	x.p_strength=my_str;
	x.p_level=my_lev;
	x.p_sex=psexall(mynum);
	x.p_score=my_sco;
	if(parser.zapped) return;
	bprintf("\nSaving %s\n",globme);
	putpers(globme,&x);
}

 validname(name)
 char *name;
    {
    long a;
    if(resword(name)){bprintf("Sorry I cant call you that\n");return(0);  }
    if(strlen(name)>10)
       {
       return(0);
       }
    a=0;
    while(name[a])
       {
       if(name[a]==' ')
          {
          return(0);
          }
       a++;
       }
    if(fobn(name)!=-1)
       {
      bprintf("I can't call you that , It would be confused with an object\n");
       return(0);
       }
    return(1);
    }

resword(name)
{
if(!strcmp(name,"The")) return(1);
if(!strcmp(name,"Me")) return(1);
if(!strcmp(name,"Myself")) return(1);
if(!strcmp(name,"It")) return(1);
if(!strcmp(name,"Them")) return(1);
if(!strcmp(name,"Him")) return(1);
if(!strcmp(name,"Her")) return(1);
if(!strcmp(name,"Someone")) return(1);
return(0);
}


"""
