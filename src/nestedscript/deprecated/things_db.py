class ThingsDb:
    things = dict()
    instances = []

    @classmethod
    def add_thing(cls, thing):
        cls.things[thing.thing_name] = thing

    @classmethod
    def add_instance(cls, instance):
        cls.instances.append(instance)

    @classmethod
    def get_thing(cls, thing_name):
        return cls.things.get(thing_name, cls.things.get('error'))

    @classmethod
    def get_child(cls, child_name):
        if not isinstance(child_name, str):
            return child_name
        if child_name[0] != '.':
            return child_name

        group = cls.things[child_name[1:]]
        if not group:
            return None
        return group.children

    @classmethod
    def clean_all(cls):
        for item in cls.things.values():
            item.children = sum([child.add_group(child) for child in item.children if child is not None])

    @classmethod
    def check_missing(cls):
        all_contents = []
        for thing in cls.things:
            for children in thing.children:
                if not isinstance(children, str):
                    all_contents += children
                else:
                    all_contents.append(children)

        all_missing = []
        for this_content in all_contents:
            if this_content[0] == '.':
                this_content = this_content[1:]
            this_content = this_content.split(',')
            this_content = this_content[0]
            if this_content and not cls.things[this_content]:
                all_missing.append(this_content)
        # allMissing=allMissing.filter(function(elem,pos) {return allMissing.indexOf(elem)==pos;}); # remove duplicates

        print("Things that are linked to, but don't exist :\n")
        print("\n".join(all_missing))

    @classmethod
    def add_children(cls, instance, children):
        for thing in children:
            child = thing()
            child.parent = instance
            instance.children.append(child)
