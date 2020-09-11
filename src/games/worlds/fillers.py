def show_names(decorated):
    def f(item_class, *args, count=10, **kwargs):
        title = item_class.__name__
        gender = kwargs.get('gender')

        print()
        print(f'{title} ({gender})' if gender else title)
        for itemId in range(count):
            item = decorated(item_class, *args, **kwargs)
            print(itemId + 1, str(item))
    return f


@show_names
def fill(item_class, *args, **kwargs):
    return item_class.generate(*args, **kwargs)


@show_names
def describe(item_class, *args, **kwargs):
    item = item_class()
    return item.description
