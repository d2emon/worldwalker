from ..errors import CommandError
from ..services.descriptions import DescriptionService
from .world_item import WorldItem


"""
Object structure

Name,
Long Text 1
Long Text 2
Long Text 3
Long Text 4
statusmax
Value
flags (0=Normal 1+flannel)


Objinfo

Loc
Status
Stamina
Flag 1=carr 0=here


Objects held in format

[Short Text]
[4 Long texts]
[Max State]


Objects in text file in form

Stam:state:loc:flag
"""


