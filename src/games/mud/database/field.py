class Field:
    def __init__(
        self,
        validators=(),
    ):
        self.validators = validators

    def validate(self, value):
        """

        :param value:
        :return:
        """
        return all(validator(value) for validator in self.validators)
