from .obdat import objects


RESERVED = [
    "the",
    "me",
    "myself",
    "it",
    "them",
    "him",
    "her",
    "someone",
    "there",
]


def test_reserved(name):
    if name.lower() in RESERVED:
        raise ValueError("Sorry I cant call you that")


def find_object_by_name(name):
    search = name.lower()
    for item in objects:
        if item.o_name == search:
            return item
    return None


def test_valid_username(username):
    """

    :param username:
    :return:
    """
    if len(username) > 10:
        raise ValueError()
    if " " in username:
        raise ValueError()
    test_reserved(username)
    if find_object_by_name(username) is not None:
        raise ValueError("I can't call you that , It would be confused with an object")
