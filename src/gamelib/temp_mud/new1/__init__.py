"""
Extensions section 1
"""
from ..magic import randperc
from ..newuaf import NewUaf
from ..parse.messages import Message
from ..support import Item, Player


def teletrap(new_channel):
    Message(
        Tk,
        Tk,
        MSG_GLOBAL,
        user.location_id,
        "\001s{name}\001{name} has left.\n\001".format(name=Tk.globme),
    ).send()
    Message(
        Tk,
        Tk,
        MSG_GLOBAL,
        new_channel,
        "\001s{name}\001{name} has arrived.\n\001".format(name=Tk.globme),
    ).send()
    user.go_to_location(new_channel)


def on_flee_event():
    for item_id in range(ObjSys.numobs):
        item = Item(item_id)
        if item.is_carried_by(user) and not item.is_worn_by(user):
            item.set_location(user.location, 0)


"""
teletrap(newch)
long newch;
{
       char block[200];
       sprintf(block,"%s%s%s%s%s","\001s",globme,"\001",globme," has left.\n\001");
       user.send_message(globme,globme,-10000,user.location_id,block);
       sprintf(block,"%s%s%s%s%s","\001s",globme,"\001",globme," has arrived.\n\001");
       user.send_message(globme,globme,-10000,newch,block);
       user.location = newch
}

on_flee_event()
{
	extern long  numobs;
	long ct=0;
	while(ct<numobs)
	{
		if((ct.is_carried_by(user))&&(!Item(ct).is_worn_by(user)))
		{
			Item(ct).set_location(user.location, 0);
		}
		ct++;
	}
}
"""