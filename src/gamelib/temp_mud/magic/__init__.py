import random


def random_percent():
    return random.randrange(100)


"""
 ressurcom()
    {
    long bf[32];
    long a,b;
    extern char wordbuf[];
    if(not user.is_wizard)
       {
       bprintf("Huh ?\n");
       return;
       }
    if(brkword()== -1)
       {
       bprintf("Yes but what ?\n");
       return;
       }
    a = Item.find(
        wordbuf,
        available=True,
        mode_0=True,
        destroyed=parser.user.is_wizard
    )
    if(a== -1)
       {
       bprintf("You can only ressurect objects\n");
       return;
       }
    if(not Item(a).is_destroyed)
       {
       bprintf("That already exists\n");
       return;
       }
    Item(a).create();
    Item(a).set_location(user.location_id,0);
    sprintf(bf,"The %s suddenly appears\n",Item(a).name);
    user.send_message("","",-10000,user.location_id,bf);
    }
"""