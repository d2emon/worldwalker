from games.mud.database import validators, field


class User:
    __RESERVED_WORDS = [
        "the",
        "me",
        "myself",
        "it",
        "them",
        "him",
        "her",
        "someone",
        "there",
    ]
    fields = {
        'username': field.Field(
            validators=(
                validators.validate_max_length(10),
                validators.validate_spaces(),
                validators.validate_reserved_words(__RESERVED_WORDS),
                validators.validate_match_with_object(),
            ),
        ),
    }
