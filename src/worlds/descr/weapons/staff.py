import random


class DataItem:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name


class GeneratorData:
    def __init__(self, values):
        self.data = [DataItem(item_id, value) for item_id, value in enumerate(values)]

    def generate(self):
        return random.choice(self.data)


def generate_providers(providers_data):
    return {key: GeneratorData(values) for key, values in providers_data.items()}


data = {
    'nm2': [
        "elegant", "exceptional", "exclusive", "expensive", "extraordinary", "first-class", "first-rate", "gorgeous",
        "grand", "magnificent", "marvelous", "primal", "rare", "refined", "solid", "superior", "supreme", "the finest",
        "unique", "wicked"
    ],
    'nm3': [
        "iron", "steel", "mithril", "gold", "silver", "brass", "bronze", "titanium", "adamantium", "obsidian", "acacia",
        "alder", "ash", "aspen", "baobab", "basswood", "baywood", "beech", "birch", "bitterwood", "blackthorn",
        "blackwood", "buckeye", "cedar", "cherry", "chestnut", "cycad", "cypress", "dogwood", "ebony wood",
        "elder wood", "elm", "fiddlewood", "fir", "firethorn", "hackberry", "hawthorn", "hazel", "hazelnut wood",
        "hemlock", "hickory", "hornbeam", "inkwood", "ironbark", "ironwood", "juniper wood", "kingwood", "lancewood",
        "larch", "laurel", "magnolia", "mahogany", "maidenwood", "mangrove wood", "maple", "medlar", "oak", "oleander",
        "pine", "poisonwood", "poplar", "redbud", "redwood", "reed", "rosewood", "rowan", "sandalwood", "senna",
        "sequoia", "spruce", "strongbark", "sycamore", "toadwood", "vine", "walnut", "willow", "yew", "yucca"
    ],
    'nm4': [
        "astonishing", "elegant", "exalted", "glorious", "grand", "grandiose", "imposing", "impressive", "incredible",
        "magnificent", "majestic", "marvelous", "monumental", "noble", "sensational", "spectacular", "stunning",
        "sublime", "superb", "terrific", "wonderful"
    ],
    'nm5': [
        "A broad, smooth staff widens at the ends and contracts at the handle",
        "A delicate cloth has been wrapped around the entire length of this straight staff, except for the handle",
        "A glowing, lava-like pattern make the otherwise simple staff look like it glows, even at the handle",
        "A glowing, seemingly liquid line wraps around the entire staff like blood and covers the handle",
        "A scaled cord wraps tightly around the entire staff like a snake, only opening up to leave enough room at the "
        "handle",
        "A single cord wraps around the entire staff to create a twisting look and a strong handle",
        "A single decorated cord wraps around the entire staff including the handle",
        "A thick ominous cord wraps around the staff and forms a handle",
        "A web-like pattern covers the entire staff with the exception of the handle",
        "An intricate intertwining metal cord forms a decorative piece which stops just above the handle",
        "Carved and curved pieces create an elegant staff base with a strong handle",
        "Carved runes cover this jagged, twisting staff from top to bottom, leaving only the handle untouched",
        "Crystal formations protrude at several points along the staff and mark the position of the handle",
        "Crystal-like shards are merged into the staff, allowing light to flow through and making it glow. Only the "
        "handle is kept smooth",
        "Curved, talon-like extensions protrude just above and below the handle",
        "Feathers decorate the otherwise simple staff but leave the handle uncovered",
        "Flame-like decorations dance and wrap around the entire staff with the exception of the handle",
        "Gilded decorations wrap around the entire rod and mark the position of the handle",
        "Glowing orbs are integrated along the entire staff with the exception of the handle",
        "Glowing runes are carved along the entire staff with the exception of the handle",
        "Glowing, glass-like formations are fused into the entire length of the staff with the exception of the handle",
        "Intertwining pieces form an open root-like appearance and only close tightly at the handle",
        "Intertwining roots and floral designs wrap around the staff, but leave the handle uncovered",
        "Intertwining roots wrap around the entire staff, but open up more at the handle",
        "Most of the staff has been polished and smoothened. Cloth ribbons with runes have been attached just below "
        "the handle",
        "Most of the staff is simple, except for round extensions at various points, including above and below the "
        "handle",
        "Most of the staff is simple, except for several diamond shaped extensions above and below the handle",
        "Playfully intertwining shafts only ever touch to form the handle",
        "Rows of rings are carved along the entire staff and mark the position of the handle",
        "Rows of spikes cover the otherwise simple staff design, with the exception of the handle",
        "Rows upon rows of glowing rings wrap around the entire staff with the exception of the handle",
        "Rows upon rows of small gems cover the simple, straight staff except for the handle",
        "Several intertwining cords only come together once to form a handle",
        "The entire length of this staff has been carefully painted with intricate patterns, leaving only the handle "
        "untouched",
        "The entire length of this straight staff has been wrapped in smooth leather, with the exception of the handle",
        "The entirety of this staff has been decorated with gilded patterns, only leaving the handle untouched",
        "The entirety of this straight staff has been carved with seemingly glowing runes, with the exception of the "
        "handle",
        "The staff has been smoothened and strengthened at core positions, including the handle",
        "The staff itself has been polished, smoothened and strengthened at the handle",
        "The staff itself has the appearance of a thin tree-like structure with a simple handle",
        "The staff itself is simple and undecorated with the exception of the handle",
        "The staff starts of wide and narrows continuously towards the end, it only widens once more to form a handle",
        "Thick, decorative extensions protrude at several points along the staff including the handle",
        "This staff widens greatly at both ends, but makes sure to be thin enough in the middle to form a handle",
        "Thorn-like extensions protrude in a random pattern along the entire staff with the exception of the handle",
        "Twisting and turning, this staff is rough and unrefined except for the handle",
        "Two glowing, intertwining rods wrap around the entire staff and form a strong handle",
        "Two rows of gems at either side decorate the otherwise simple staff, but stop at the handle",
        "Two straight rods never touch except for the point where they form a handle",
        "Two twin rods dance around each other and only touch to form a handle"
    ],
    'nm6': [
        "wrapped in a strong, but smooth silk", "wrapped in tight leather for a firm grip",
        "wrapped in emblazoned leather", "wrapped in embellished cloth", "decorated with small carved runes",
        "wrapped in an inscribed cloth cord", "strengthened and polished", "strengthened with a metal coating",
        "decorated with a crosshatched cord", "left untouched completely", "adorned with tiny gems for a firm grip",
        "decorated with an ancient text carved into it", "painted with a simplistic style",
        "smoothened and strengthened", "emblazoned with magical runes", "wrapped in reptilian leather",
        "decorated with scale-like stubs", "strengthened with decorated metal",
        "wrapped in leather with gilded linings", "wrapped in cloth with gilded linings",
        "covered in thick bulges for more grip", "wrapped in exotic animal skin", "covered in a marble pattern",
        "decorated with carved patterns", "decorated with a few crystals"
    ],
    'nm7': [
        "a barbed shield shape", "a bird wing shaped decoration", "a bone shape", "a claw-like ornament",
        "a crafted animal claw", "a crafted animal skull", "a crafted dragon head", "a crafted raven head",
        "a crafted reptilian tail", "a crafted skull", "a crafted wolf head", "a crown-shaped ornament",
        "a curved blade shape", "a curvy twirl", "a decorative eye", "a decorative floral ornament",
        "a decorative handle-shape", "a decorative reptilian tail", "a decorative snake",
        "a decorative, flame-shaped piece", "a dull blade shape", "a dull tip", "a fan-shape",
        "a gnarled, root-like stub", "a hammerhead", "a heart shape", "a key shape", "a leaf-like ornament",
        "a lightning bolt", "a long scythe shape", "a mirrored marquise shape", "a pointed fan", "a rounded cross",
        "a rounded feather shape", "a shield shape", "a short marquise shape", "a simple orb", "a simple stub",
        "a simple twirl", "a simple, reinforced stub", "a skull-shaped decorative piece", "a smooth crescent",
        "a smooth spearhead", "a spiked crescent", "a spiky cross", "a spiky feather shape", "a spiky wing shape",
        "a spiral shape", "a star shape", "a talon shape", "a teardrop shape", "a thick decorated cylinder",
        "a thick decorated prism", "a thick diamond shape", "a thick ring", "a thick sphere", "a tightly twisted stub",
        "a twisting tip", "an angel wing shaped decoration", "an angular hook-shape",
        "an elaborate intertwining art piece", "an elongated crescent", "an elongated crystal shape",
        "an elongated marquise shape", "an open diamond", "an ornate snowflake", "an ornate, crafted spider",
        "an ornate, gilded decorative piece", "intertwining crafted feathers", "intertwining wave shapes",
        "layered scythe shapes", "root-like decorations", "several intertwining spikes", "three spikes",
        "two decorative, intertwining snakes", "two small wings"
    ],
    'nm8': [
        "wood", "mithril", "adamantium", "metal", "glass", "crystal", "wood", "wood", "obsidian"
    ],
    'nm9': [
        "a crosshatched, tightly wrapped ribbon with gems on the crossing parts",
        "a glowing layer of what seems to be some kind of paint",
        "a glowing line that twirls around it all and adds a magical sense to the look",
        "a glowing orb carefully encased in prongs shaped liked a spider",
        "a gnarly root that gently wraps around, adding a natural element to the overall appearance",
        "a large gem with the appearance of an eye, said to allow vision of wherever the staff is",
        "a large gem wrapped gently encased in gilded prongs",
        "a large orb that seems to give off electric charges at seemingly random times",
        "a large, multi-colored tassel with a big, bright gem attached just above it",
        "a mosaic of rough, multi-colored crystal shards of various sizes",
        "a mosaic of smooth, multi-colored gems. All roughly the same size",
        "a smooth layer of paint, giving the edges a glowing appearance",
        "a smooth ribbon that wraps around and is engraved with glowing symbols",
        "a straight gilded lining on each side, with several small gems at equal distance of each other",
        "a thick ring inscribed with various magical runes",
        "a thin gilded lining that wraps around in a seemingly random fashion",
        "an elegantly encased orb that glows even in the darkest darkness",
        "an encased gem which seems to change colors every so often, perhaps due to magical powers",
        "an ornately encased orb with the appearance of the moon said to grant lunar powers",
        "beads hanging from similar colored, seemingly glowing threads",
        "blade-shaped gems in a fan-shaped pattern symmetrically placed on two sides",
        "bright crystals place in such a way that they mimic a flame in their appearance",
        "bright, jagged crystals that give off a soft humming sound whenever magic is used",
        "countless metal spikes, sharp enough to do damage, but small enough to be relatively harmless",
        "countless spiky gems, giving the appearance of glowing barbs",
        "crafted leaves in various shapes and painted in vibrant colors",
        "crystal shards in a symmetric pattern, giving it a frozen, snowflake-like look",
        "curved blade shapes, position together in a fan or wing-like pattern",
        "dozens of small round gems giving it a gentle glow and a smooth texture",
        "embedded crystals in the shape of leaves, they seem to be living and thriving on magical powers",
        "embedded crystals that are said to grow the more times magic is used while wielding the staff",
        "flat and smooth metal plates in a floral pattern, painted in natural colors",
        "gilded linings and a few small gems that seem to float gently above the surface of the staff",
        "glowing gems, which will glow more brightly when magic is used while the staff is wielded",
        "glowing orbs that orbit around at gentle speeds at all times",
        "glowing, triangular gems with smaller gems floating around them",
        "horn-like pieces, shaped in twirling motions and painted in darker colors",
        "intricate designs made with curving shapes and bright colors",
        "intricate designs made with thin, spiky shapes that intertwine and dance around each other",
        "intricate gilded pattern design, said to have secret meanings only known to the wielder",
        "intricate swirling patterns, in some cases almost wave-like and in others more like a whirlpool",
        "intricately painted patterns, said to be an ancient text with an unknown meaning",
        "intricately crafted feathers painted in vibrant colors",
        "intricately carved shapes in a symmetric pattern",
        "many small pearls in a simple pattern and each in a different color",
        "many smaller gems that glisten in the light, making it seem like they hold magical properties",
        "several crystals floating in a symmetric pattern, always gently turning in a circle",
        "several dangling ribbons inscribed with ancient texts said to hold protective powers",
        "several floating crystals, gently floating round and round in an almost hypnotic fashion",
        "several orbs that seem to glow all on their own, even when there's no light source",
        "several runes that have been magically inscribed and are said to enhance the magic of the wielder",
        "several smaller gems, which may hold magical properties known only to the wielder",
        "several thin glowing linings, dancing around each other to form a unique pattern",
        "several triangular gems touching point to point, forming a simple yet elegant pattern",
        "sharp, dark-colored spikes, giving it a very ominous appearance",
        "small talon-like spikes in a row, giving them a spine-like appearance",
        "small tassels, each with a small gem attached to it to give them some weight",
        "thick fan-shaped ornamental pieces in a symmetric pattern",
        "thick gilded rings, each with a two gems at equal distance of each other",
        "thin, almost ribbon-like metal strips in bright colors and twirling patterns",
        "translucent crystals, carved and placed carefully to give it an almost ghostly appearance",
        "two wing shapes that gently orbit around in a soft motion",
        "various gems attached in such a way that they seem to be floating in the air",
        "vibrant bird feathers from various sources",
        "what seems to be an eternally burning, magical flame that doesn't affect the staff itself"
    ],
    'nm10': [
        "a barbed crescent shape", "a bird claw", "a butterfly shape", "a crescent shape", "a cross", "a crown",
        "a curved point", "a demonic skull", "a dragon head", "a floral shape", "a fork-like shape", "a harpoon-shape",
        "a heart shape", "a horned animal skull", "a horned skull", "a jagged crescent shape", "a key shape",
        "a kite shape", "a lantern-like shape", "a laurel shape", "a perfect circle", "a pointy star shape",
        "a quatrefoil shape", "a raven head", "a reptilian tail", "a rhombus shape", "a root-like shape",
        "a rounded star shape", "a scythe-like shape", "a sharp, jagged fan", "a shield shape", "a skull",
        "a smooth hook", "a smooth oval", "a smooth point", "a spider-like shape", "a spiky cross",
        "a spiky laurel shape", "a sun shape", "a tentacled orb", "a twirling laurel shape", "a winged eye",
        "a winged orb", "a winged skull", "a winged star shape", "a wrapped orb", "a wreath shape",
        "an abstract design of curves", "an abstract design of spikes", "an abstract design of twirls",
        "an abstract symmetrical design", "an animal claw", "an animal head", "an elongated crescent",
        "an elongated ellipse shape", "an elongated marquise shape", "an elongated scythe-like shape",
        "an encased cross", "an encased crystal", "an encased heart", "an encased shield", "an encased sphere",
        "an encased star", "an eye", "an eye in a star", "an insect-like shape", "an open heart shape",
        "an open sphere", "angel wings", "animal horns", "bird wings", "blade-like wings", "demonic wings",
        "long, thin spikes", "stacked crescent shapes", "stacked crowns", "stacked scythe shapes",
        "stacked wing shapes", "thin, curving blades", "two stacked orbs"
    ],
}

providers = generate_providers(data)


class DescriptionGenerator:
    def __init__(self):
        self.nm1 = 0
        self.generators = {
            'nm1': self.generate_nm1,
            'nm1b': self.generate_nm1b,
            'nm2': providers['nm2'].generate,
            'nm3': providers['nm3'].generate,
            'nm4': providers['nm4'].generate,
            'nm5': providers['nm5'].generate,
            'nm6': providers['nm6'].generate,
            'nm7': providers['nm7'].generate,
            'nm8': providers['nm8'].generate,
            'nm9': providers['nm9'].generate,
            'nm10': providers['nm10'].generate,
            'nm11': providers['nm2'].generate,
            'nm12': providers['nm8'].generate,
            'nm13': providers['nm9'].generate,
        }
        self.templates = {
            'name1': "{nm1} centimeters ({nm1b} inches) of {rnd2} {rnd3} form the base of this {rnd4} staff. {rnd5}, "
                     "which has been {rnd6}.",
            'name2': "The bottom ends in {rnd7} made of {rnd8} and has been decorated with {rnd9}.",
            'name3': "The top is made out of {rnd11} {rnd12} and has been crafted into {rnd10}, which has been "
                     "decorated with {rnd13}.",
        }

        self.data = dict()
        self.generate()

    def generate_nm1(self):
        self.nm1 = random.randrange(160, 220)
        return self.nm1

    def generate_nm1b(self):
        return int(self.nm1 * .393701)

    def verify(self, key):
        if key == 'nm13':
            return self.data.get('nm13') != self.data.get('nm9')
        if self.data.get(key) is None:
            return False
        return True

    def generate(self):
        to_generate = filter(lambda k: self.verify(k), self.generators.keys())

        if not to_generate:
            return self.data

        for key in to_generate:
            self.data[key] = self.generators[key]()

        return self.generate()

    @property
    def names(self):
        return {key: template.format(**self.data) for key, template in self.templates.items()}

    @property
    def text(self):
        return "{name1}\n\n{name2}\n\n{name3}".format(**self.names)
