from .items import Item
from .users import User


def validate_required(
    message='',
):
    def validator(value):
        if not value:
            raise ValueError(message)
        return value
    return validator


def validate_max_length(
    max_length,
    message='',
):
    def validator(value):
        if len(value) > max_length:
            raise ValueError(message)
    return validator


def validate_characters(
    illegal,
    message='',
):
    def validator(value):
        if value and any(c in value for c in illegal):
            raise ValueError(message)
        return value
    return validator


def validate_az(
    message='',
):
    def validator(value):
        for c in value.lower():
            if c < 'a' or c > 'z':
                raise ValueError(message)
        return value
    return validator


def validate_reserved_words(
    reserved_words,
    message='Sorry I cant call you that',
):
    def validator(value):
        if value.lower() in reserved_words:
            raise ValueError(message)
    return validator


def validate_match_with_object(
    message='I can\'t call you that , It would be confused with an object',
):
    def validator(value):
        if Item.find_by_name(value) is not None:
            raise ValueError(message)
    return validator


def validate_user(
    message='',
):
    def validator(value):
        try:
            return User.fields['username'](value)
        except ValueError:
            raise ValueError(message)
    return validator


#


def validate_spaces(
    message='',
):
    return validate_characters('', message)
