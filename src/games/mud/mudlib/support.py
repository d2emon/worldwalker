import logging
from games.mud.world import items
from games.mud.models.item import Item
from games.mud.models.pc import PlayerCharacter
from . import files
from . import object

# extern FILE* openlock();

"""
Some more basic functions

Note

state(obj)
setstate(obj,val)
destroy(obj)

are elsewhere
"""

# extern OBJECT objects[];


def system_log(message):
    # service = open(LOF_FILE, 'a') or loseme("Log fault : Access Failure")
    # service.append(f'{time()}:  {message}')
    logging.info(message)


#


# Items


def get_item_location_flag(item_id):
    """
    Get item location flag
    """
    return Item.load(item_id).location_flag


def set_item_location_flag(item_id, value):
    """
    Set item location flag
    """
    item = Item.load(item_id)
    item.set_location(item.location_id, value)


def get_item_location_id(item_id):
    """
    Get item location id
    """
    return Item.load(item_id).location_id


def set_item_location(item_id, location_id, location_flag):
    """
    Set item location
    """
    Item.load(item_id).set_location(location_id, location_flag)


def get_item_name(item_id):
    """
    Get item name
    """
    return Item.load(item_id).name


def get_item_description(item_id, state):
    """
    Get item description
    """
    return Item.load(item_id).get_description(state)


def get_item_max_state(item_id):
    """
    Get item max state
    """
    return Item.load(item_id).max_state


def get_item_movable(item_id):
    """
    Get item movable
    """
    return Item.load(item_id).is_movable


def get_item_base_value(item_id):
    """
    Get item base value
    """
    return Item.load(item_id).base_value


def get_item_is_destroyed(item_id):
    """
    Get item destroyed
    """
    return Item.load(item_id).is_destroyed


def get_item_is_available(item_id):
    """
    Get item available
    """
    my_num = 0
    return Item.load(item_id).available_for(my_num)


def get_item_is_spare(item_id):
    """
    Get item spare
    """
    return not Item.load(item_id).is_destroyed


def create_item(item_id):
    """
    Create item
    """
    Item.load(item_id).create()


def get_item_flag(item_id, flag_id):
    """
    Get item flag
    """
    return Item.load(item_id).get_flag(flag_id)


def set_item_flag(item_id, flag_id):
    """
    Set item flag
    """
    Item.load(item_id).set_flag(flag_id, True)


def clear_item_flag(item_id, flag_id):
    """
    Clear item flag
    """
    Item.load(item_id).set_flag(flag_id, False)


def get_item_value(item_id, value_id):
    """
    Get item value
    """
    return Item.load(item_id).get_value(value_id)


def set_item_value(item_id, value_id, value):
    """
    Set item value
    """
    Item.load(item_id).set_value(value_id, value)


def has_any_items(mask):
    """
    User has any items by mask
    """
    return Item.by_mask(**mask)


# PC


def get_character_name(character_id):
    """
    Get character name
    """
    return PlayerCharacter.load(character_id).name


def get_character_channel_id(character_id):
    """
    Get character channel id
    """
    return PlayerCharacter.load(character_id).channel_id


def set_character_channel_id(character_id, value):
    """
    Set character channel id
    """
    PlayerCharacter.load(character_id).channel_id = value


def get_character_level(character_id):
    """
    Get character level
    """
    return PlayerCharacter.load(character_id).level


def set_character_level(character_id, value):
    """
    Set character level
    """
    PlayerCharacter.load(character_id).level = value


def get_character_strength(character_id):
    """
    Get character strength
    """
    return PlayerCharacter.load(character_id).strength


def set_character_strength(character_id, value):
    """
    Set character strength
    """
    PlayerCharacter.load(character_id).strength = value


def get_character_visible(character_id):
    """
    Get character visible
    """
    return PlayerCharacter.load(character_id).visible


def set_character_visible(character_id, value):
    """
    Set character visible
    """
    PlayerCharacter.load(character_id).visible = value


def get_character_flags(character_id):
    """
    Get character flags
    """
    return PlayerCharacter.load(character_id).flags


def set_character_flags(character_id, value):
    """
    Set character flags
    """
    PlayerCharacter.load(character_id).flags = value


def get_character_sex(character_id):
    """
    Get character sex
    """
    return PlayerCharacter.load(character_id).sex


def set_character_sex(character_id, value):
    """
    Set character sex
    """
    PlayerCharacter.load(character_id).sex = value


def get_character_event_id(character_id):
    """
    Get character event id
    """
    return PlayerCharacter.load(character_id).event_id


def set_character_event_id(character_id, value):
    """
    Set character event id
    """
    PlayerCharacter.load(character_id).event_id = value


def get_character_weapon_id(character_id):
    """
    Get character weapon id
    """
    return PlayerCharacter.load(character_id).weapon_id


def set_character_weapon_id(character_id, value):
    """
    Set character weapon id
    """
    PlayerCharacter.load(character_id).weapon_id = value


def get_character_helping_id(character_id):
    """
    Get character helping id
    """
    return PlayerCharacter.load(character_id).helping_id


def set_character_helping_id(character_id, value):
    """
    Set character helping id
    """
    PlayerCharacter.load(character_id).helping_id = value


def get_character_helper(character_id):
    """
    Get character helper
    """
    return next(PlayerCharacter.load(character_id).helpers, None)


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


def __psetflg(ch, x):
    """
psetflg(ch,x)
long ch;
long x;
{
   # extern long ublock[];
   ublock[16*ch+9]|=(1<<x);
}
    """
    pass


def __pclrflg(ch, x):
    """
pclrflg(ch,x)
long ch;
long x;
{
   # extern long ublock[];
   ublock[16*ch+9]&=~(1<<x);
}
"""
    pass


def __ptstbit(ch, x):
    """
ptstbit(ch,x)
long ch;
long x;
{
   return(ptstflg(ch,x));
}
    """
    pass


def __ptstflg(ch, x):
    """
ptstflg(ch,x)
long ch;
long x;
{
   # extern long ublock[];
   # extern char globme[];
   if((x==2)&&(strcmp(globme,"Debugger")==0)) return(1<<x);
   return(ublock[16*ch+9]&(1<<x));
}
"""
