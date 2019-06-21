from datetime import datetime
from .errors import ServiceError


class World:
    __reset_objects = []
    __reset_time = None

    objects = []
    objinfo = []
    item_ids = len(objects)  # 196

    ublock = []
    player_ids = len(ublock)  # 49

    first_message = 0
    last_message = 0
    __messages = []

    @classmethod
    def load(cls):
        raise NotImplementedError()

    @classmethod
    def save(cls):
        raise NotImplementedError()

    @classmethod
    def resetplayers(cls):
        for mobile in MOBILES:
            mobile.reset()
        for player in Player.players()[16 + len(MOBILES):]:
            player.reset()

    @classmethod
    def get_message_id(cls, message_id):
        return 2 * message_id - cls.first_message

    # Tk
    @classmethod
    def get_message(cls, message_id):
        return cls.__messages[cls.get_message_id(message_id)]

    # Unknown
    @classmethod
    def add_message(cls, message):
        message_id = cls.get_message_id(cls.last_message)
        cls.__messages[message_id] = message
        cls.last_message += 1
        return message_id

    # Tk
    @classmethod
    def get_messages(cls, first=None, last=None):
        if last is None:
            last = cls.last_message
        if first is None or first < 0:
            first = last

        for message_id in range(first, last):
            yield cls.get_message(message_id)

    @classmethod
    def clear_old_messages(cls):
        cls.load()
        for i in range(100):
            cls.__messages[i] = cls.__messages[100 + i]
        cls.first_message += 100
        return cls.first_message

    @classmethod
    def reset_time(cls):
        return "Last Reset At {}\n".format(cls.__reset_time)

    @classmethod
    def reset(cls):
        user.broadcast("Reset in progress....\nReset Completed....\n")
        cls.objects = cls.__reset_objects
        cls.__reset_time = datetime.now()
        cls.resetplayers()

    @classmethod
    def system_reset(cls):
        if scale() != 2:
            raise CommandError("There are other people on.... So it wont work!\n")
        if cls.__reset_time and datetime.now() - cls.__reset_time < 3600:
            raise CommandError("Sorry at least an hour must pass between resets\n")
        cls.reset()

    # Parse
    @classmethod
    def __system(cls, command):
        raise NotImplementedError

    @classmethod
    def __keys_set_back(cls):
        raise NotImplementedError

    @classmethod
    def __keys_set_up(cls):
        raise NotImplementedError

    @classmethod
    def remote_editor(cls):
        cls.show_buffer()
        try:
            cls.chdir(ROOMS)
        except ServiceError:
            yield "Warning: Can't CHDIR\n"

        return cls.__system("/cs_d/aberstudent/yr2/hy8/.sunbin/emacs")

    @classmethod
    def tss(cls, command):
        World.save()

        with cls.__keys():
            return cls.__system(command)

    @classmethod
    def honeyboard(cls):
        return cls.__system("/cs_d/aberstudent/yr2/hy8/bt")


"""
/* Fast File Controller v0.1 */

FILE *filrf=NULL;  /* - = not open */

closeworld()
{
	extern FILE *filrf;
        extern long objinfo[],numobs,ublock[];
	if(filrf==NULL) return;
	sec_write(filrf,objinfo,400,4*numobs);
	sec_write(filrf,ublock,350,16*48);
	filrf.disconnect()
	filrf= NULL;
}

FILE *openworld()
{
	extern FILE *filrf;
        extern long objinfo[],numobs,ublock[];
	if(filrf!=NULL) return(filrf);
	filrf=connect("/usr/tmp/-iy7AM","r+");
	if(filrf==NULL)
	   crapup("Cannot find World file");
	sec_read(filrf,objinfo,400,4*numobs);
	sec_read(filrf,ublock,350,16*48);
	return(filrf);
}

"""