from . import genders


__GENDERS = {
    genders.NEUTRAL: 0,
    genders.MALE: 1,
    genders.FEMALE: 2,
}


def show_names(decorated):
    def f(item_class, *args, **kwargs):
        items = decorated(item_class, *args, **kwargs)
        title = item_class.__name__
        gender = kwargs.get('gender')

        print()
        print(f'{title} ({gender})' if gender else title)
        for itemId, item in enumerate(items):
            print(itemId + 1, str(item))
    return f


@show_names
def fill(item_class, *args, count=10, gender=None, **kwargs):
    args = (__GENDERS.get(gender), *args) if gender is not None else args
    return [item_class.generate(*args) for _ in range(count)]


@show_names
def describe(item_class, *args, **kwargs):
    item = item_class()
    return item.description
