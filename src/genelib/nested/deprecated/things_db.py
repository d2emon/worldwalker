class ItemsDb:
    generators = {}
    items = []

    # Generators

    @classmethod
    def add_generator(cls, item_generator):
        cls.generators[item_generator.__class__.__name__] = item_generator

    @classmethod
    def get_generator(cls, name):
        return cls.generators.get(name, cls.generators.get('ErrorItem'))

    # Items

    @classmethod
    def add_item(cls, item):
        cls.items.append(item)

    # Children

    @classmethod
    def add_children(cls, item, children):
        for item_generator in children:
            child = item_generator()
            child.parent = item
            item.children.append(child)

    @classmethod
    def get_child(cls, name):
        if not isinstance(name, str):
            return name

        if name[0] != '.':
            return name

        group = cls.generators.get(name[1:])
        if not group:
            return None
        return group.children

    # Cleanup and check missing

    @classmethod
    def clean_all(cls):
        for item in cls.generators.values():
            item.children = [child.add_group(child) for child in item.children if child is not None]

    @classmethod
    def __contents(cls):
        for item_generator in cls.generators:
            for children in item_generator.children:
                if not isinstance(children, str):
                    yield from children
                else:
                    yield children

    @classmethod
    def __missing(cls):
        for content in cls.__contents():
            if content[0] == '.':
                content = content[1:]
            content = content.split(',')
            content = content[0]
            if content and not cls.generators.get(content):
                yield content
        # allMissing=allMissing.filter(function(elem,pos) {return allMissing.indexOf(elem)==pos;});
        # remove duplicates

    @classmethod
    def check(cls):
        print("Things that are linked to, but don't exist :\n")
        for m in cls.__missing():
            print(m)
