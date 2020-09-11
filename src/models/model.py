class Model:
    __DATA = {}

    fields = []

    class Field:
        def __init__(self, name, default=None):
            self.name = name
            self.default = default

        def get_value(self, model):
            return model.values.get(self.name)

        def set_value(self, model, value):
            model.values[self.name] = value

    class IndexField(Field):
        pass

    class LookupField(Field):
        def __init__(self, name, lookup_model):
            super().__init__(name)
            self.lookup_model = lookup_model

        def get_value(self, model):
            item_id = super().get_value(model)
            model = self.lookup_model.get(item_id)
            return model

        def set_value(self, model, value):
            super().set_value(model, value and value.id)

    def __init__(self, **kwargs):
        self.values = {f.name: kwargs.get(f.name, f.default) for f in self.fields}

    def __getattribute__(self, name):
        if name == 'fields':
            return object.__getattribute__(self, name)

        field = next((f for f in self.fields if f.name == name), None)
        return field.get_value(self) if field is not None else object.__getattribute__(self, name)

    def __setattr__(self, key, value):
        field = next((f for f in self.fields if f.name == key), None)
        return field.set_value(self, value) if field is not None else super().__setattr__(key, value)

    def save(self):
        return self.add(self)

    @property
    def __index_field(self):
        return next(field for field in self.fields if isinstance(field, self.IndexField))

    @property
    def id(self):
        return self.values.get(self.__index_field.name)

    @classmethod
    def __data(cls):
        if cls.__name__ not in cls.__DATA.keys():
            cls.__DATA[cls.__name__] = {}
        return cls.__DATA[cls.__name__]

    @classmethod
    def get(cls, item_id):
        return cls(**cls.__data().get(item_id, {}))

    @classmethod
    def delete(cls, item_id):
        del cls.__data()[item_id]

    @classmethod
    def add(cls, item):
        cls.__data()[item.id] = {**item.values}
        return item

    @classmethod
    def all(cls):
        return (cls(**data) for data in cls.__data().values())
