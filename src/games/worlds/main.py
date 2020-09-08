GENDERS = {
    0: chr(9893),
    1: chr(9794),
    2: chr(9792),
}


def __names(items):
    for itemId, item in enumerate(items):
        print(itemId + 1, str(item))


def generate_list(title, item_class, *args):
    print("\n{}".format(title))
    __names([item_class.generate(*args) for _ in range(10)])


def generate_gendered(title, item_class, genders):
    for gender in genders:
        generate_list(f'{title} ({GENDERS[gender]})', item_class, gender)


def generate_description(title, item_class):
    item = item_class()
    print(f'\n{title}\n{item.description}')
