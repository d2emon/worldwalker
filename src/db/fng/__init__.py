from .descr import DATA as DESCRIPTIONS
from .fantasyNames import FANTASY_NAMES_DATA

from models.fng.text_generator import TextGenerator
from models.fng.data_group import DataGroup
from models.fng.data_item import DataItem


DATA = {
    **FANTASY_NAMES_DATA,
    **DESCRIPTIONS,
}

for text_generator_slug in DATA.keys():
    text_generator = TextGenerator(slug=text_generator_slug).save()
    # print(text_generator.values)
    generator_data = DATA.get(text_generator_slug) or {}
    for group_slug in generator_data.keys():
        group = DataGroup(slug=group_slug, text_generator=text_generator.id).save()
        # print(group.values, group_slug, text_generator)
        group_data = generator_data.get(group_slug) or {}
        for item_id, text in enumerate(group_data):
            DataItem(item_id=item_id, text=text, group=group.id).save()
