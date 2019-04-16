import random


class DataItem:
    def __init__(self, item_id, text):
        self.item_id = item_id
        self.text = text


class DataProvider:
    data = []

    @classmethod
    def shuffled(cls):
        result = [DataItem(item_id, item) for item_id, item in enumerate(cls.data)]
        random.shuffle(result)
        return iter(result)


class NameGenerator:
    providers = []

    def __init__(self):
        self.data = self.reset()

    def __iter__(self):
        return self

    def __next__(self):
        self.reset()
        name = self.test_swear(self.name())
        if not name:
            return next(self)
        return name

    def reset(self):
        self.data = [provider.shuffled() for provider in self.providers]
        return self.data

    def name(self):
        return "Name"

    @classmethod
    def test_swear(cls, name):
        swear = [
            "alah", "allah", "anal", "anilingus", "anus", "apeshit", "arse", "arsehole", "ass", "asshole", "assmunch",
            "autoerotic", "babeland", "balls", "ballsack", "bangbros", "bareback", "barenaked", "bastard", "bastardo",
            "bastinado", "beaner", "beaners", "bestiality", "biatch", "bigtits", "bimbos", "birdlock", "bitch",
            "bitches", "black", "bloody", "blowjob", "blumpkin", "bollock", "bollocks", "bollok", "bondage", "boner",
            "boob", "boobs", "bugger", "bukkake", "bulldyke", "bullshit", "bum", "bunghole", "busty", "butt",
            "buttcheeks", "butthole", "buttplug", "cameltoe", "camgirl", "camslut", "camwhore", "clit", "clitbeard",
            "clitoris", "cloaka", "clusterfuck", "cock", "cocks", "coon", "coons", "cornhole", "crap", "creampie",
            "cum", "cumming", "cunt", "damn", "darkie", "daterape", "deepthroat", "dick", "dildo", "doggy", "dolcett",
            "domination", "dominatrix", "dommes", "dryhump", "dyke", "ecchi", "ejaculation", "erotic", "erotism",
            "escort", "eunuch", "fag", "fagget", "faggit", "faggot", "faggut", "faghet", "faghit", "faghot", "faghut",
            "fecal", "feck", "felch", "felching", "fellate", "fellatio", "feltch", "femdom", "fetish", "figging",
            "fingerbang", "fingering", "fisting", "flange", "footjob", "frotting", "fuck", "fuckin", "fucking",
            "fucktard", "fucktards", "fudgepacker", "futanari", "gangbang", "gaysex", "genitals", "goatcx", "goatse",
            "god", "goddamn", "gokkun", "goodpoop", "googirl", "goregasm", "grope", "groupsex", "guro", "handjob",
            "hardcore", "hell", "hentai", "homo", "homoerotic", "honkey", "hooker", "humping", "incest", "intercourse",
            "jackoff", "jailbait", "jerk", "jerkoff", "jigaboo", "jiggaboo", "jiggerboo", "jizz", "juggs", "kike",
            "kinbaku", "kinkster", "kinky", "knobbing", "knobend", "kum", "labia", "lmao", "lmfao", "lolita",
            "masturbate", "milf", "muff", "nambla", "nawashi", "neeger", "neegger", "negger", "negro", "neonazi",
            "nieger", "niegger", "niga", "nigar", "niger", "nigga", "niggar", "niggas", "niggaz", "nigger", "nigges",
            "niggir", "niggis", "niggor", "niggos", "niggur", "niggus", "nigher", "nighes", "nignog", "nigra",
            "nimphomania", "nipple", "nipples", "nude", "nudity", "nympho", "nymphomania", "obama", "octopussy", "omg",
            "omorashi", "oral", "orgasm", "orgy", "paedo", "paki", "panties", "panty", "pedo", "pegging", "penis",
            "pis", "piss", "pissing", "pisspig", "playboy", "ponyplay", "poof", "poon", "poontang", "poop", "porn",
            "porno", "prick", "pube", "pubes", "punany", "pussy", "queaf", "queef", "queer", "quim", "raghead", "rape",
            "raping", "rapist", "rectum", "rimjob", "rimming", "sadism", "santorum", "scat", "schlong", "scissoring",
            "scrotum", "semen", "sex", "sexo", "sexy", "shaved", "shemale", "shibari", "shit", "shitblimp", "shitty",
            "shota", "shrimping", "skeet", "slanteye", "slut", "smegma", "smut", "snatch", "sodomize", "sodomy", "spic",
            "splooge", "spooge", "spunk", "strapon", "suck", "sucks", "suicide", "sultry", "swastika", "swinger",
            "threesome", "throating", "tiits", "tit", "tits", "titties", "titty", "topless", "tosser", "towelhead",
            "trani", "tranie", "tranni", "trannie", "tranny", "trany", "trennie", "tubgirl", "turd", "tushy", "twat",
            "twink", "twinkie", "upskirt", "urethra", "urophilia", "vagina", "vibrator", "voyeur", "vulva", "wank",
            "wetback", "whore", "wtf", "yaoi", "yiffy",
        ]
        if name.lower() in swear:
            return None
        return name

    @classmethod
    def unique(cls, item, unique_with, data):
        while item.text == unique_with.text:
            item = next(data)
        return item


class Named:
    name_generators = [NameGenerator()]

    def __init__(self, name=''):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def name_generator(cls):
        return random.choice(cls.name_generators)

    @classmethod
    def generate(cls, count=10):
        return [cls(next(cls.name_generator()).title()) for _ in range(count)]
