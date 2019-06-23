"""
Two Phase Game System
"""
from ..errors import CrapupError
from ..keys import Keys
from ..screen import Screen
from ..syslog import syslog


def main(user_id, name):
    if name == "Phantom":
        name = "The " + name

    print("Entering Game ....\n")
    print("Hello {}\n".format(name))
    syslog("GAME ENTRY: {}[{}]".format(name, user_id))

    screen = Screen(name)
    with Keys:
        try:
            screen.main()
        except KeyboardInterrupt:
            return screen.on_quit()
        except CrapupError as e:
            return screen.on_crapup(e)
        except SystemExit:
            return screen.on_error()
