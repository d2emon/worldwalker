from .errors import CrapupError, ServiceError, CommandError
from .item import Item
from .location import Location
from .message import Broadcast, Message, Silly, MSG_WIZARD, MSG_GLOBAL, MSG_FLEE
from .player import Player
from .world import World


class User:
    wd_there = ""

    class NewUaf:
        level = 0
        score = 0
        sex = 0
        strength = 0

    class Blood:
        fighting = None
        in_fight = 0

        @classmethod
        def stop_fight(cls):
            cls.in_fight = 0
            cls.fighting = None

    def __init__(self, name):
        self.in_setup = False

        self.has_farted = False
        self.__player_id = None

        self.__location_id = 0

        self.__is_on = False

        self.__updated = 0

        self.rd_qd = False

        self.__in_ms = "has arrived."
        self.__out_ms = ""
        self.__mout_ms = "vanishes in a puff of smoke."
        self.__min_ms = "appears with an ear-splitting bang."
        self.__here_ms = "is here"

        self.__message_id = None
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def is_wizard(self):
        return self.NewUaf.level > 9

    @property
    def is_god(self):
        return self.NewUaf.level > 9999

    @property
    def can_carry(self):
        max_items = self.max_items
        if max_items is None:
            return True
        return sum(not item.is_destroyed and item.is_carried_by(self.player) for item in Item.items()) < max_items

    @property
    def is_dark(self):
        if self.is_wizard:
            return False
        if not self.location.is_dark:
            return False
        for item in (item for item in Item.items() if item.is_light):
            if is_here(item):
                return False
            if item.owner is not None and item.owner.location == self.__location_id:
                return False
        return True

    @property
    def location(self):
        return Location(self.__location_id)

    @property
    def max_items(self):
        if not self.player.is_wizard:
            return None
        if self.player.level < 0:
            return None
        return self.player.level + 5

    @property
    def player(self):
        return Player(self.__player_id)

    def set_wd_there(self, zone, location_id):
        self.wd_there = zone + " " + location_id

    @property
    def enemy(self):
        return Player(self.Blood.fighting)

    def check_fight(self):
        if self.Blood.fighting is not None:
            if not self.enemy.exists:
                self.Blood.stop_fight()
            if self.enemy.location != self.__location_id:
                self.Blood.stop_fight()

        if self.Blood.in_fight:
            self.Blood.in_fight -= 1

    def read_messages(self, reset_after_read=False):
        yield from self.get_messages()

        self.update()
        eorte()
        rdes = 0
        tdes = 0
        vdes = 0
        if reset_after_read:
            self.__message_id = None

    def reset_location_id(self, is_random=False):
        if is_random:
            self.__location_id = -5 if randperc() > 50 else -183
        else:
            self.__location_id = -5

    def reset_message_id(self):
        self.__message_id = None
        self.__put_on()

    def go_to_channel(self, channel_id):
        World.load()
        self.player.location = channel_id
        self.look_in(self.location)

    def __put_on(self):
        self.__is_on = False
        World.load()
        if Player.fpbn(self.name) is not None:
            raise CrapupError("You are already on the system - you may only be on once at a time")

        self.__player_id = next((player.player_id for player in PLAYERS if not player.is_alive), None)
        if self.__player_id is None:
            raise CrapupError("\nSorry AberMUD is full at the moment\n")

        self.player.put_on(self.name, self.__location_id, self.__message_id)
        self.__is_on = True

    def loose(self):
        sig_aloff()
        # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        self.in_setup = False

        World.load()
        dumpitems()
        if self.player.visible < 10000:
            self.send_message(
                self,
                MSG_WIZARD,
                0,
                "{} has departed from AberMUDII\n".format(self.name)
            )
        self.player.remove()
        World.save()

        if not self.__zapped:
            saveme()
        chksnp()

    def update(self):
        if abs(self.__message_id - self.__updated) < 10:
            return

        World.load()
        self.player.position = self.__message_id
        self.__updated = self.__message_id

    def look_in(self, location):
        World.save()

        if self.__ail_blind:
            yield "You are blind... you can't see a thing!\n"

        if self.is_wizard:
            location.show_name(self)

        try:
            un1 = openroom(location.location_id, "r")
            # xx1
            xxx = False
            location.load_exits(un1)
            if self.is_dark:
                fclose(un1)
                yield "It is dark\n"

                World.load()
                on_look()
                return

            for s in un1:
                if s == "#DIE":
                    if self.__ail_blind:
                        rewind(un1)
                        self.__ail_blind = False
                        # xx1()
                    elif self.NewUaf.level > 9:
                        yield "<DEATH ROOM>\n"
                    else:
                        self.loose()
                        raise CrapupError("bye bye.....\n")
                elif s  == "#NOBR":
                    self.brief = False
                    xxx = self.brief
                else:
                    if not self.__ail_blind and not xxx:
                        yield "{}\n".format(s)
                    xxx = self.brief
        except FileNotFoundError:
            yield "\nYou are on channel {}\n".format(location.location_id)
        fclose(un1)

        World.load()
        if not self.__ail_blind:
            lisobs()
            if self.mode == 1:
                lispeople()
        yield "\n"
        on_look()

    # Support
    def is_available(self, item):
        if self.is_here(item):
            return True
        return item.is_carried_by(self.player)

    def has_any(self, mask):
        items = Item.items()
        items = (item for item in items if item.is_carried_by(self.__player_id) or item.is_here(self.__player_id))
        return any(item for item in items if item.test_mask(mask))

    # Unknown
    # Messages
    def send_message(self, to_user, code, channel_id, message):
        Message(to_user, self, code, channel_id, message).send(self)

    def broadcast(self, message):
        self.rd_qd = True
        Broadcast(message).send(self)

    def silly(self, message):
        Silly(self, message).send(self)

    def get_messages(self):
        try:
            World.load()
            return Message.messages(self.__message_id)
        except ServiceError:
            raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")

    def process_messages(self, *messages):
        for message in messages:
            self.__message_id = message.message_id
            if message.code < -3:
                yield from gamrcv(message, self.name.lower())
            else:
                yield message.text

    # For actions
    def quit_game(self):
        if self.Disease.is_force:
            raise CommandError("You can't be forced to do that\n")

        yield from self.read_messages()

        if self.Blood.in_fight:
            raise CommandError("Not in the middle of a fight!\n")

        yield "Ok"
        World.load()
        self.send_message(
            self,
            MSG_GLOBAL,
            self.__location_id,
            "{} has left the game\n".format(self.name)
        )
        self.send_message(
            self,
            MSG_WIZARD,
            0,
            "[ Quitting Game : {} ]\n".format(self.name)
        )
        dumpitems()
        self.player.die()
        self.player.remove()
        World.save()
        self.__location_id = 0

    def flee(self):
        if not self.Blood.in_fight:
            return

        if Item(32).iscarrby(self.__player_id):
            raise CommandError("The sword won't let you!!!!\n")

        self.send_message(
            self,
            MSG_GLOBAL,
            self.__location_id,
            "\001c{}\001 drops everything in a frantic attempt to escape\n".format(self.name),
        )
        self.send_message(
            self,
            MSG_FLEE,
            self.__location_id,
            "",
        )

        self.NewUaf.score -= self.NewUaf.score / 33  # loose 3%
        self.calibme()
        self.Blood.in_fight = None
        self.on_flee_event()

    def go_in_direction(self, direction_id):
        if self.Blood.in_fight > 0:
            raise CommandError("You can't just stroll out of a fight!\n"
                               "If you wish to leave a fight, you must FLEE in a direction\n")
        if Item(32).iscarrby(self.player) and Player(25).exists and Player(25).location == self.__location_id:
            raise CommandError("\001cThe Golem\001 bars the doorway!\n")

        self.Disease.crippled.check()

        new_location = ex_dat[direction_id]
        if 999 < new_location < 2000:
            """
       auto long  drnum,droff;
       drnum=newch-1000;
       droff=drnum^1;/* other door side */
       if(state(drnum)!=0)
          {
      if (strcmp(Item(drnum).name,"door")||isdark()||strlen(Item(drnum).description))==0)
              {
              bprintf("You can't go that way\n");
              /* Invis doors */
              }
              else
              bprintf("The door is not open\n");
          return;
          }
       newch=Item(droff).location;
            """
            pass
        if new_location == -139:
            """
       if((!iswornby(113,mynum))&&(!(iswornby(114,mynum)))&&(!iswornby(89,mynum)))
          {
          bprintf("The intense heat drives you back\n");
          return;
          }
       else
          bprintf("The shield protects you from the worst of the lava stream's heat\n");
            """
            pass
        if direction_id == 2:
            """
         if(((i=fpbns("figure"))!=mynum)&&(i!=-1)&&(Player(i).location==curch)&&!iswornby(101,mynum)&&!iswornby(102,mynum)&&!iswornby(103,mynum))
            {
            bprintf("\001pThe Figure\001 holds you back\n");
            bprintf("\001pThe Figure\001 says 'Only true sorcerors may pass'\n");
            return;
            }
            """
            pass
        if new_location >= 0:
            raise CommandError("You can't go that way\n")

        self.send_message(
            self,
            MSG_GLOBAL,
            self.__location_id,
            "\001s{user.player.name}\001{user.name} has gone {direction} {user.out_ms}.\n\001".format(
                user=self,
                direction=exittxt[direction_id],
            ),
        )
        self.__location_id = new_location
        self.send_message(
            self,
            MSG_GLOBAL,
            self.__location_id,
            "\001s{user.name}\001{user.name}{user.in_ms}.\n\001".format(
                user=self,
                direction=exittxt[direction_id],
            ),
        )
        self.trapch(self.__location_id)
