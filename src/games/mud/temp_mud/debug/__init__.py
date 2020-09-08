import logging


def show_user(user):
    logging.debug(
        """
name:\t\t\t%s
score:\t\t\td
strength:\t\t%d
sex:\t\t\t%d
level:\t\t\t%d
visible:\t\t%d
position:\t\t%d
show_players:\t%d

data:\t\t\t%s
        """,
        user.name,
        # self.score,
        user.strength,
        user.sex,
        user.level,
        user.visible,
        user.message_id,
        user.show_players,
        [
            user.name,
            # 2
            # 3

            user.location,
            user.message_id,
            0,  # 6
            user.strength,

            user.visible,
            user.sex,
            user.level,
            user.weapon,

            0,  # 12
            0,  # 13
            0,  # 14
            0,  # 15
        ],
    )
    # logging.debug("in_setup:\t%d", self.in_setup)


def show_list(text):
    # logging.debug(text)
    print("".join(text))
