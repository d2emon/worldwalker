from genelib import DataProvider, NameGenerator, Named


class Nm1(DataProvider):
    data = [
        "", "", "", "", "b", "d", "g", "h", "m", "n", "r", "s", "sh", "w", "y", "z"
    ]


class Nm2(DataProvider):
    data = [
        "a", "o", "u", "a", "o", "u", "a", "o", "u", "a", "o", "u", "a", "o", "u", "a", "o", "u", "a", "o", "u", "a",
        "o", "u", "a", "o", "u", "a", "o", "u", "i", "i", "e", "e", "e", "e", "e", "e", "ae", "aa", "ao", "au", "oa",
        "oo", "ou", "ua", "uo", "uu"
    ]


class Nm3(DataProvider):
    data = [
        "b", "bb", "bd", "bl", "bn", "g", "gg", "gn", "gy", "gt", "h", "hn", "hl", "l", "ll", "lm", "lfr", "ln", "lb",
        "m", "mn", "mm", "ml", "md", "my", "n", "nn", "nb", "ng", "nl", "nt", "nsh", "nth", "ny", "st", "ss", "sl",
        "sz", "zl", "zy", "zn"
    ]


class Nm4(DataProvider):
    data = [
        "a", "o", "u", "a", "o", "u", "a", "o", "u", "a", "o", "u", "a", "o", "u", "i", "i", "e", "e", "e", "e", "e",
        "e", "ao", "ie", "ia", "iu", "ua", "ue"
    ]


class Nm5(DataProvider):
    data = [
        "b", "bb", "c", "d", "f", "g", "h", "l", "ld", "ll", "n", "nd", "ndr", "ng", "ns", "nz", "r", "s", "ss", "v"
    ]


class Nm6(DataProvider):
    data = [
        "", "", "", "", "d", "h", "l", "m", "n", "r", "s"
    ]


class BaseZaratanNameGenerator(NameGenerator):
    """
    Zaratan are giant sea turtles, big enough to support a small island ecosystem on their shells. As a result they're
    often mistaken for islands, especially when they're in the middle of the ocean, and their movement is difficult to
    detect.

    Zaratan are common in many works of fiction, but vary a lot in terms of personality, purpose, and any meaning they
    may have. In some cases they're wise, in some they're aggressive, and in others they might simply be docile beings
    swimming across the oceans. Unfortunately there wasn't much to work with in terms of names, but the term zaratan
    does seem to come from Spanish.

    For this generator I mostly focused on bigger sounding names, often with more melodic and gentle tones. But I also
    included Spanish influences, as well as some other influences for a wider variety of possible names. The names will
    generally still have the same large and docile feel to them, but there's plenty to pick from on both ends of the
    spectrum.
    """
    providers = [
        Nm1,
        Nm2,
        Nm3,
        Nm4,
        Nm5,
        Nm6,
    ]

    def name_all(self):
        names = [
            next(self.data[0]),
            next(self.data[1]),
            next(self.data[2]),
            next(self.data[3]),
            next(self.data[5]),
        ]

        while names[2].text in (names[0].text, names[4].text):
            names[2] = next(self.data[2])

        return names

    def name(self):
        return "".join([name.text for name in self.name_all()])


class ZaratanNameGenerator1(BaseZaratanNameGenerator):
    pass


class ZaratanNameGenerator2(BaseZaratanNameGenerator):
    def name(self):
        names = self.name_all()
        names.append(next(self.data[4]))
        names.append(next(self.data[1]))

        while names[5].text in (names[2].text, names[4].text):
            names[5] = next(self.data[4])

        return "".join([
            names[0].text,
            names[1].text,
            names[2].text,
            names[3].text,
            names[5].text,
            names[6].text,
            names[4].text,
        ])


class Zaratan(Named):
    name_generators = [
        ZaratanNameGenerator1(),
        ZaratanNameGenerator2(),
    ]
