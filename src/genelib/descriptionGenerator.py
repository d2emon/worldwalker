class DescriptionGenerator:
    def __init__(self, providers):
        self.providers = providers
        self.generators = dict()
        self.rules = dict()
        self.templates = dict()
        self.text = ""

    @classmethod
    def unique(cls, key1, key2):
        def f(data):
            return data.get(key1) != data.get(key2)
        return f

    def verify(self, key, data):
        if data.get(key) is None:
            return False
        rule = self.rules.get(key)
        if rule is not None:
            return rule(data)
        return True

    def generate_items(self, **data):
        to_generate = list(filter(lambda k: not self.verify(k, data), self.generators.keys()))

        if not to_generate:
            return data

        for key in to_generate:
            provider_id = self.generators[key]
            data[key] = self.providers[provider_id].generate()

        return self.generate_items(**data)

    def generate_templates(self, **data):
        items = self.generate_items(**data)
        return {key: template.format(**items) for key, template in self.templates.items()}

    def generate(self, **data):
        templates = self.generate_templates(**data)
        return self.text.format(**templates)
