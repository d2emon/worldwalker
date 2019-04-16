from genelib import DataProvider, NameGenerator, Named


class Nm1(DataProvider):
    data = [
        "", "", "", "", "", "b", "ch", "dz", "dj", "g", "gy", "h", "j", "k", "ky", "l", "m", "n", "r", "s", "sz", "sh",
        "t", "th", "v", "z"
    ]


class Nm2(DataProvider):
    data = [
        "a", "e", "i", "o", "u", "a", "o", "u"
    ]


class Nm3(DataProvider):
    data = [
        "dd", "h", "k", "l", "ll", "m", "n", "r", "s", "t", "z", "dd", "h", "k", "kk", "l", "ll", "lr", "m", "n", "ng",
        "nr", "nz", "r", "rr", "s", "sh", "sr", "t", "ts", "vr", "y", "z"
    ]


class Nm4(DataProvider):
    data = [
        "", "", "c", "hn", "hl", "l", "m", "n", "ng", "r", "rs", "s", "sh"
    ]


class Nm4b(DataProvider):
    data = [
        "h", "k", "l", "ll", "m", "n", "r", "s", "t", "z"
    ]


class Nm5(DataProvider):
    data = [
        "", "", "", "", "", "f", "gy", "h", "k", "ky", "l", "m", "n", "ph", "r", "s", "sh", "th", "w", "y", "z"
    ]


class Nm6(DataProvider):
    data = [
        "a", "e", "i", "o", "u", "a", "e", "i"
    ]


class Nm7(DataProvider):
    data = [
        "b", "f", "g", "h", "k", "l", "ll", "m", "n", "r", "rr", "s", "t", "w", "z", "b", "f", "g", "gy", "h", "hn",
        "hl", "k", "l", "ll", "m", "n", "ng", "nn", "r", "rr", "rl", "ry", "rs", "s", "sh", "t", "ty", "th", "w", "z"
    ]


class Nm8(DataProvider):
    data = [
        "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "h", "hn", "l", "m", "n", "ng", "ph", "s", "sh",
        "th", "y"
    ]


class Nm9(DataProvider):
    data = [
        "b", "f", "g", "h", "k", "l", "ll", "m", "n", "r", "rr", "s", "t", "w", "z"
    ]


class Nm10(DataProvider):
    data = [
        "", "", "", "", "", "", "f", "g", "gy", "h", "k", "ky", "l", "m", "n", "ph", "r", "s", "sh", "th", "v", "w",
        "y", "z"
    ]


class Nm11(DataProvider):
    data = [
        "a", "e", "i", "o", "u", "a"
    ]


class Nm12(DataProvider):
    data = [
        "b", "dd", "g", "h", "k", "kk", "l", "ll", "m", "n", "nn", "r", "rr", "s", "t", "w", "y", "z", "b", "dd", "g",
        "gy", "h", "hn", "k", "kk", "l", "ll", "lr", "m", "n", "ng", "nn", "nr", "r", "rr", "ry", "s", "sh", "sr", "t",
        "th", "ts", "vr", "w", "y", "z"
    ]


class Nm13(DataProvider):
    data = [
        "", "", "", "", "", "", "", "", "h", "hl", "hn", "l", "m", "n", "ng", "ph", "r", "rs", "s", "sh", "th"
    ]


class Nm14(DataProvider):
    data = [
        "b", "dd", "g", "h", "k", "kk", "l", "ll", "m", "n", "nn", "r", "rr", "s", "t", "w", "y", "z"
    ]


class BaseYetiNameGenerator(NameGenerator):
    """
    Yetis are ape-like humanoids who supposedly inhabit the Himalayan regions and are part of popular folklore,
    religion and mythologies. There are many variants in other regions too, like Bigfoot, the Yeren, the Yowie and so
    on.

    Yetis and similar creatures aren't often given personal names, in many cases because they're the only specimen
    believed to exist. This made creating a name generator a little tricky, but since these creatures do inhabit
    specific regions of the world I decided to take inspiration from those regions to create naming conventions. I
    focused primarily on the Himalayan regions, but also took some inspiration for some of the lesser known variants of
    'yeti' out there, like the before mentioned Yeren and Yowie.
    """
    providers = [
        Nm1,
        Nm2,
        Nm3,
        Nm4,
        Nm5,
        Nm6,
        Nm7,
        Nm8,
        Nm9,
        Nm10,
        Nm11,
        Nm12,
        Nm13,
        Nm14,  #
        Nm4b,
    ]


class BaseFemaleYetiNameGenerator(BaseYetiNameGenerator):
    def names(self):
        return [
            next(self.data[4]),
            next(self.data[5]),
            next(self.data[6]),
            next(self.data[5]),
            next(self.data[7]),
        ]


class BaseMaleYetiNameGenerator(BaseYetiNameGenerator):
    def names(self):
        return [
            next(self.data[0]),
            next(self.data[1]),
            next(self.data[2]),
            next(self.data[1]),
            next(self.data[3]),
        ]


class BaseNeutralYetiNameGenerator(BaseYetiNameGenerator):
    def names(self):
        return [
            next(self.data[9]),
            next(self.data[10]),
            next(self.data[11]),
            next(self.data[10]),
            next(self.data[12]),
        ]


class FemaleYetiNameGenerator1(BaseFemaleYetiNameGenerator):
    def name(self):
        names = self.names()

        names[2] = self.unique(names[2], names[0], self.data[6])

        if names[0].item_id < 5:
            while names[4].item_id < 15 or names[2].text == names[4].text:
                names[4] = next(self.data[7])

        return "".join([name.text for name in names])


class FemaleYetiNameGenerator2(BaseFemaleYetiNameGenerator):
    def name(self):
        names = self.names()
        names.append(next(self.data[8]))
        names.append(next(self.data[5]))

        names[2] = self.unique(names[2], names[0], self.data[6])
        names[4] = self.unique(names[4], names[5], self.data[7])
        names[5] = self.unique(names[5], names[2], self.data[8])

        return "".join([
            names[0].text,
            names[1].text,
            names[2].text,
            names[3].text,
            names[5].text,
            names[6].text,
            names[4].text,
        ])


class FemaleYetiNameGenerator3(BaseFemaleYetiNameGenerator):
    def name(self):
        names = self.names()
        names.append(next(self.data[8]))
        names.append(next(self.data[5]))

        names[2] = self.unique(names[2], names[0], self.data[6])
        names[4] = self.unique(names[4], names[2], self.data[7])
        names[5] = self.unique(names[5], names[2], self.data[8])

        return "".join([
            names[0].text,
            names[1].text,
            names[5].text,
            names[6].text,
            names[2].text,
            names[3].text,
            names[4].text,
        ])


class MaleYetiNameGenerator1(BaseMaleYetiNameGenerator):
    def name(self):
        names = self.names()

        names[2] = self.unique(names[2], names[0], self.data[2])

        if names[0].item_id < 5:
            while names[4].item_id < 2 or names[2] == names[4]:
                names[4] = next(self.data[3])

        return "".join([name.text for name in names])


class MaleYetiNameGenerator2(BaseMaleYetiNameGenerator):
    def name(self):
        names = self.names()
        names.append(next(self.data[14]))
        names.append(next(self.data[1]))

        names[2] = self.unique(names[2], names[0], self.data[2])
        names[4] = self.unique(names[4], names[5], self.data[3])
        names[5] = self.unique(names[5], names[2], self.data[14])

        return "".join([
            names[0].text,
            names[1].text,
            names[2].text,
            names[3].text,
            names[5].text,
            names[6].text,
            names[4].text,
        ])


class MaleYetiNameGenerator3(BaseMaleYetiNameGenerator):
    def name(self):
        names = self.names()
        names.append(next(self.data[14]))
        names.append(next(self.data[1]))

        names[2] = self.unique(names[2], names[0], self.data[2])
        names[4] = self.unique(names[4], names[2], self.data[3])
        names[5] = self.unique(names[5], names[2], self.data[14])

        return "".join([
            names[0].text,
            names[1].text,
            names[5].text,
            names[6].text,
            names[2].text,
            names[3].text,
            names[4].text,
        ])


class YetiNameGenerator1(BaseNeutralYetiNameGenerator):
    def name(self):
        names = self.names()

        names[2] = self.unique(names[2], names[0], self.data[11])

        if names[0].item_id < 5:
            while names[4].item_id < 15 or names[2] == names[4]:
                names[4] = next(self.data[12])

        return "".join([name.text for name in names])


class YetiNameGenerator2(BaseNeutralYetiNameGenerator):
    def name(self):
        names = self.names()
        names.append(next(self.data[13]))
        names.append(next(self.data[10]))

        names[2] = self.unique(names[2], names[0], self.data[11])
        names[4] = self.unique(names[4], names[5], self.data[12])
        names[5] = self.unique(names[5], names[2], self.data[13])

        return "".join([
            names[0].text,
            names[1].text,
            names[2].text,
            names[3].text,
            names[5].text,
            names[6].text,
            names[4].text,
        ])


class YetiNameGenerator3(BaseNeutralYetiNameGenerator):
    def name(self):
        names = self.names()
        names.append(next(self.data[13]))
        names.append(next(self.data[10]))

        names[2] = self.unique(names[2], names[0], self.data[11])
        names[4] = self.unique(names[4], names[5], self.data[12])
        names[5] = self.unique(names[5], names[2], self.data[13])

        return "".join([
            names[0].text,
            names[1].text,
            names[5].text,
            names[6].text,
            names[2].text,
            names[3].text,
            names[4].text,
        ])


class Yeti(Named):
    name_generators = [
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator2(),
        FemaleYetiNameGenerator2(),
        FemaleYetiNameGenerator3(),
        FemaleYetiNameGenerator3(),
    ]

    female_name_generators = [
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator1(),
        FemaleYetiNameGenerator2(),
        FemaleYetiNameGenerator2(),
        FemaleYetiNameGenerator3(),
        FemaleYetiNameGenerator3(),
    ]

    male_name_generators = [
        MaleYetiNameGenerator1(),
        MaleYetiNameGenerator1(),
        MaleYetiNameGenerator1(),
        MaleYetiNameGenerator1(),
        MaleYetiNameGenerator1(),
        MaleYetiNameGenerator1(),
        MaleYetiNameGenerator2(),
        MaleYetiNameGenerator2(),
        MaleYetiNameGenerator3(),
        MaleYetiNameGenerator3(),
    ]

    neutral_name_generators = [
        YetiNameGenerator1(),
        YetiNameGenerator1(),
        YetiNameGenerator1(),
        YetiNameGenerator1(),
        YetiNameGenerator1(),
        YetiNameGenerator1(),
        YetiNameGenerator2(),
        YetiNameGenerator2(),
        YetiNameGenerator3(),
        YetiNameGenerator3(),
    ]
