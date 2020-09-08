from .items import Item


def validate_max_length(max_length):
    def validator(value):
        if len(value) > max_length:
            raise ValueError('')
    return validator


def validate_spaces():
    def validator(value):
        if ' ' in value:
            raise ValueError('')
    return validator


def validate_reserved_words(reserved_words):
    def validator(value):
        if value.lower() in reserved_words:
            raise ValueError('Sorry I cant call you that')
    return validator


def validate_match_with_object():
    def validator(value):
        if Item.find_by_name(value) is not None:
            raise ValueError('I can\'t call you that , It would be confused with an object')
    return validator
