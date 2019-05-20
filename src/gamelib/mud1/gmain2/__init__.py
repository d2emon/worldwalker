"""
Program starts Here!

This forms the main loop of the code, as well as calling
all the initialising pieces
"""
import sys
from ...file_services import ResetN, Nologin, Exe, MotD, BanFile, Pfl
from ...mud_services import Mud1Services
from ..errors import CrapupError
from ..gmainstubs import GMainStubs, cls, getty, syslog, validname, qcrypt, dcrypt
from ..gmlnk import quick_start, talker
# from ..stdio import *
# from ..system import *


class GMain2:
    # lump = ''
    namegiv = False
    namegt = ''
    qnmrq = False
    # usrnam = ''

    @classmethod
    def set_name(cls, name):
        cls.qnmrq = True
        GMainStubs.ttyt = 0
        cls.namegt = name
        cls.namegiv = True


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
    def verify_server():
        Mud1Services.validate_host(env.host)
        print()
        print()
        print()
        print()
        Mud1Services.check_nologin()

    def parse_args(option):
        """
        Now check the option entries

        -n(name)

        :return:
        """
        if option == 'N':
            return GMain2.set_name(args[1][2:])

    def show_logo():
        getty()
        time = Mud1Services.get_time()
        cls()
        print()
        print("                         A B E R  M U D")
        print()
        print("                  By Alan Cox, Richard Acott Jim Finnis")
        print()
        print(time['created'])
        print(time['elapsed'])

    def show_motd():
        cls()
        input(Mud1Services.get_message_of_the_day())
        print()
        print()

    try:
        verify_server()
        if len(args) == 2 and args[1][0] == '-':
            parse_args(args[1][1].upper())
        if not GMain2.namegiv:
            show_logo()
        # Check if banned first
        Mud1Services.chkbndid(env.user_id)
        # Does all the login stuff
        user = login(env)
        if not GMain2.qnmrq:
            show_motd()
        syslog("Game entry by {} : UID {}".format(user.username, env.user_id))  # Log entry
        if GMain2.qnmrq:
            quick_start(user)
        else:
            talker(user)  # Run system
        crapup("Bye Bye")  # Exit
    except CrapupError as e:
        crapup(e)


def login(user):
    """
    The whole login system is called from this

    Get the user name

    :return:
    """
    if not GMain2.namegiv:
        username = input("By what name shall I call you ?\n*")[:15].strip()
    else:
        username = GMain2.namegt
        GMain2.namegiv = 0

    """
    Check for legality of names
    """
    try:
        Mud1Services.validate_username(username)
    except ValueError as e:
        print(e)
        return login(user)

    user_data = Mud1Services.logscan(username)
    if user_data is None:
        # If he/she doesnt exist
        if input("\nDid I get the name right {} ?".format(username)).lower()[0] == 'n':
            print()
            return login(user)  # Check name

    return logpass(username)  # Password checking


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
