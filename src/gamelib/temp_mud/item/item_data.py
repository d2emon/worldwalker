from ..world import World


class BaseItemData:
    @property
    def item_id(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def description(self):
        raise NotImplementedError()

    @property
    def max_state(self):
        raise NotImplementedError()

    @property
    def flannel(self):
        raise NotImplementedError()

    @property
    def base_value(self):
        raise NotImplementedError()


class ItemData(BaseItemData):
    __objects = []

    @property
    def item_id(self):
        raise NotImplementedError()

    @property
    def __object(self):
        return self.__objects[self.item_id]

    @property
    def state(self):
        raise NotImplementedError()

    @state.setter
    def state(self, value):
        raise NotImplementedError()

    # Support
    @property
    def name(self):
        return self.__object.name

    @property
    def description(self):
        return self.__object.description[self.state]

    @property
    def max_state(self):
        return self.__object.max_state

    @property
    def flannel(self):
        return self.__object.flannel

    @property
    def base_value(self):
        return self.__object.value
