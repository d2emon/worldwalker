"""
Program starts Here!

This forms the main loop of the code, as well as calling
all the initialising pieces
"""
import sys
from .. import temp, config
from ..gmainstubs import GMainStubs, cls, getty, syslog, validname, qcrypt, dcrypt
# from ..stdio import *
# from ..sys.types import *
# from ..sys.stat import *
# from ..system import *
from ...file_services import ResetN, Nologin, Exe, MotD, BanFile, Pfl


class GMain2:
    # lump = ''
    namegiv = False
    namegt = ''
    qnmrq = False
    # usrnam = ''


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def mud1(env, *args):
    """
    The initial routine

    :param env:
    :param args:
    :return:
    """
    def show_time():
        """
        Elapsed time and similar goodies

        :return:
        """
        def seconds(s):
            if s % 60 == 1:
                return "1 second"
            else:
                return "{} seconds.".format(s % 60)

        token = ResetN.connect(permissions='r')
        time = ResetN.time(token)

        if time > 24 * 60 * 60:
            return "Over a day!!!\n"  # Add a Day !
        if time < 61:
            return seconds(time)
        if time == 60:
            return "1 minute"
        if time < 120:
            return "1 minute and " + seconds(time)
        if time / 60 == 60:
            return "1 hour"
        if time < 120:
            return "{} minutes and ".format(time / 60) + seconds(time)

        if time < 7200:
            hours = "1 hour and "
        else:
            hours = "{} hours and ".format(time / 3600)

        if (time / 60) % 60 != 1:
            return hours + "{} minutes.".format((time / 60) % 60)
        else:
            return hours + "1 minute"

    """
    Check we are running on the correct host
    see the notes about the use of flock();
    and the affects of lockf();
    """
    if env.host != config.HOST_MACHINE:
        raise Exception("AberMUD is only available on {}, not on {}".format(config.HOST_MACHINE, env.host))

    print()
    print()
    print()
    print()

    """
    Check if there is a no logins file active
    """
    chknolog()

    if len(args) == 2 and args[1][0] == '-':
        """
        Now check the option entries
        
        -n(name)
        """
        option = args[1][1].upper()
        if option == 'N':
            GMain2.qnmrq = True
            GMainStubs.ttyt = 0
            GMain2.namegt = args[1][2:]
            GMain2.namegiv = True

    if not GMain2.namegiv:
        getty()

    """
    Check for all the created at stuff
    
    We use stats for this which is a UN*X system call
    """
    if not GMain2.namegiv:
        stats = Exe.get_stats()
        created = stats.date if stats is not None else "<unknown>\n"

        cls()
        print()
        print("                         A B E R  M U D")
        print()
        print("                  By Alan Cox, Richard Acott Jim Finnis")
        print()
        print("This AberMUD was created:{}".format(created))
        try:
            print("Game time elapsed: " + show_time())
        except FileNotFoundError:
            print("AberMUD has yet to ever start!!!")

    user = login(env)  # Does all the login stuff
    if not GMain2.qnmrq:
        cls()
        try:
            input(MotD.get_text())  # list the message of the day
        except Exception as e:
            input(e)
        print()
        print()
    syslog("Game entry by {} : UID {}".format(user.username, env.user_id))  # Log entry
    temp.talker(user)  # Run system
    crapup("Bye Bye")  # Exit


def login(user):
    """
    The whole login system is called from this

    :return:
    """
    def rename():
        """
        Get the user name

        :return:
        """
        if not GMain2.namegiv:
            username = input("By what name shall I call you ?\n*")[:15].strip()
        else:
            username = GMain2.namegt

        """
        Check for legality of names
        """
        GMain2.namegiv = 0

        try:
            if "." in username:
                crapup("\nIllegal characters in user name\n")

            if not username:
                raise ValueError

            chkname(username)
        except ValueError as e:
            print(e)
            return rename()

        try:
            validname(username)
        except ValueError:
            crapup("Bye Bye")

        user_data = logscan(username)
        if user_data is None:
            # If he/she doesnt exist
            a = input("\nDid I get the name right {} ?".format(username)).lower()
            c = a[0]
            if c == 'n':
                print()
                return rename()  # Check name

        return logpass(username)  # Password checking

    """
    Check if banned first
    """
    chkbndid(user.user_id)

    return rename()


def chkbndid(user_id):
    """
    Check to see if UID in banned list

    :return:
    """
    try:
        token = BanFile.connect(permissions="r+")
        for banned in BanFile.get_line(token, max_length=79):
            if banned == user_id:
                raise Exception("I'm sorry- that userid has been banned from the Game\n")
        BanFile.disconnect(token)
    except FileNotFoundError:
        return


def logscan(username):
    """
    Return block data for user or -1 if not exist

    :param username:
    :return:
    """
    try:
        token = Pfl.connect_lock(permissions="r")
    except FileNotFoundError:
        return crapup("No persona file\n")

    found = None
    for user in Pfl.get_content(token):
        decoded = dcrypt(user)
        if decoded.username.lower() == username.lower():
            found = decoded
            break
        else:
            continue
    Pfl.disconnect(token)
    return found


def logpass(username):
    """
    Main login code

    :param username:
    :return:
    """
    def try_pass(user, tries=0):
        password = input("\nThis persona already exists, what is the password ?\n*")
        print()
        if password == user.password:
            if tries < 2:
                return try_pass(user, tries + 1)
            else:
                return crapup("\nNo!\n\n")
        return user

    def reinput_password():
        password = input("*")
        print()

        try:
            if not password:
                raise ValueError()
            if "." in password:
                raise ValueError("Illegal character in password")
        except ValueError as e:
            print(e)
            return reinput_password()

        user = User(username, password)

        try:
            token = Pfl.connect_lock(permissions="a")
        except FileNotFoundError:
            return crapup("No persona file....\n")
        Pfl.add_line(token, qcrypt(user))
        Pfl.disconnect(token)
        return user

    block = logscan(username)
    if block is not None:
        result = try_pass(block)
    else:
        # this bit registers the new user
        print("Creating new persona...")
        print("Give me a password for this persona")
        result = reinput_password()
    cls()
    return result


"""
void getunm(name)
 char *name;
    {
    printf("\nUser Name:");
    fgets(name,79,stdin);
    }

void showuser()
    {
    long a;
    char name[80],block[256];
    cls();
    getunm(name);
    shu(name,block);
    printf("\nHit Return...\n");
    while(getchar()!='\n');
    }

long shu(name,block)  /* for show user and edit user */
 char *name,*block;
    {
    long a;
    long x;
    char nm[128],pw[128],pr[128],pv[128];
    a=logscan(name,block);
    if (a== -1) printf("\nNo user registered in that name\n\n\n");
    else
       {
       printf("\n\nUser Data For %s\n\n",name);
       x=scan(nm,block,0,"",".");
       x=scan(pw,block,x+1,"",".");
       printf("Name:%s\nPassword:%s\n",nm,pw);
       }
    return(a);
    }

void deluser()
{
    long a;
    char name[80],block[256];
    getunm(name);
    a=logscan(name,block);
    if (a== -1) printf("\nCannot delete non-existant user\n");
    else
    {
	delu2(name);
    }
}

void edituser()
    {
    long a;
    FILE *fl;
    char name[80],block[256],bk2[256];
    char nam2[128],pas2[128],per2[128],pr2[128];
    cls();
    getunm(name);
    a=shu(name,block);
    if (a== -1) sprintf(block,"%s%s",name,".default.E..");
    a=scan(nam2,block,0,"",".");
    a=scan(pas2,block,a+1,"",".");
    printf("\nEditing : %s\n\n",name);
    ed_fld("Name:",nam2);
    ed_fld("Password:",pas2);
    sprintf(bk2,"%s%s%s%s%s%s%s%s",nam2,".",pas2,".",".",".",".",".");
    delu2(name);
    fl=openlock(PFL,"a");
    if(fl==NULL) return;
    qcrypt(bk2,lump,strlen(bk2));
    strcpy(bk2,lump);
    fprintf(fl,"%s\n",bk2);
    disconnect(fl);
    }

void ed_fld(name,string)
 char *name,*string;
    {
    char bk[128];
    bafld:printf("%s(Currently %s ):",name,string);
    fgets(bk,128,stdin);
    if(bk[0]=='.') strcpy(bk,"");
    if(strchr(bk,'.')){printf("\nInvalid Data Field\n");goto bafld;}
    if (strlen(bk)) strcpy(string,bk);
    }
void delu2(name)   /* For delete and edit */
 char *name;
    {
    char b2[128],buff[128];
    FILE *a;
    FILE *b;
    char b3[128];
    a=openlock(PFL,"r+");
    b=openlock(PFT,"w");
    if(a==NULL) return;
    if(b==NULL) return;
    while(fgets(buff,128,a)!=0)
       {
       dcrypt(buff,lump,strlen(buff)-1);
       scan(b2,lump,0,"",".");
       strcpy(b3,name);lowercase(b3);
       if (strcmp(b3,lowercase(b2))) fprintf(b,"%s",buff);
       }
    disconnect(a);
    disconnect(b);
    a=openlock(PFL,"w");
    b=openlock(PFT,"r+");
    if(a==NULL) return;
    if(b==NULL) return;
    while(fgets(buff,128,b)!=0)
       {
       fprintf(a,"%s",buff);
       }
    disconnect(a);
    disconnect(b);
    }


void chpwd(user)   /* Change your password */
 char *user;
    {
    char block[128],data[128],pwd[80],pv[80];
    long a;
    FILE *fl;
    strcpy(data,user);
    logscan(user,block);
    strcpy(user,data);
    a=scan(data,block,0,"",".");
    a=scan(pwd,block,a+1,"",".");
    printf("\nOld Password\n*");
    fflush(stdout);
    gepass(data);
    if(strcmp(data,pwd)) printf("\nIncorrect Password\n");
    else
       {
       printf("\nNew Password\n");
       chptagn:printf("*");
       fflush(stdout);
       gepass(pwd);
       printf("\n");
       if (!strlen(pwd)) goto chptagn;
       if (strchr(pwd,',')) 
	{
		printf("Illegal Character in password\n");
		goto chptagn;
	}
       printf("\nVerify Password\n*");
       gepass(pv);
       printf("\n");
       if (strcmp(pv,pwd))
       {
		printf("\nNO!\n");
		goto chptagn;
	}
       sprintf(block,"%s%s%s%s%s%s%s%s",user,".",pwd,".",".",".",".",".");
       delu2(user);  /* delete me and tack me on end! */
       fl=openlock(PFL,"a");
       if(fl==NULL) return;
       qcrypt(block,lump,strlen(block));
       strcpy(block,lump);
       fprintf(fl,"%s\n",block);
       disconnect(fl);
       printf("Changed\n");
   }
}
"""


def crapup(ptr):
    input("\n{}\n\nHit Return to Continue...".format(ptr))
    sys.exit(1)


"""
/*
 *		This is just a trap for debugging it should never get
 *		called.
 */ 

void bprintf()
{
	printf("EEK - A function has trapped via the bprintf call\n");
	exit(0);
}
"""

def chkname(user):
    """

    :param user:
    :return:
    """
    for a in user.lower():
        if a > 'z':
            raise ValueError()
        if a < 'a':
            raise ValueError()


def chknolog():
    """

    :return:
    """
    try:
        token = Nologin.connect(permissions='r')
        error = Nologin.get_content(token)
        Nologin.disconnect(token)
        raise error
    except FileNotFoundError:
        return
