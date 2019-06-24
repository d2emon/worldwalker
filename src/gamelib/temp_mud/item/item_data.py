from ..services.items import ItemsService


class BaseItemData:
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
    @property
    def item_id(self):
        raise NotImplementedError()

    @property
    def __object(self):
        return ItemsService.get_item(item_id=self.item_id)

    @property
    def state(self):
        raise NotImplementedError()

    @state.setter
    def state(self, value):
        raise NotImplementedError()

    # Support
    @property
    def name(self):
        return self.__object.get("name")

    @property
    def description(self):
        return self.__object.get("description", [])[self.state]

    @property
    def max_state(self):
        return self.__object.get("max_state")

    @property
    def flannel(self):
        return self.__object.get("flannel")

    @property
    def base_value(self):
        return self.__object.get("value")
