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

    def get_provider(self, key):
        provider_id = self.generators.get(key)
        if not provider_id:
            return None
        return self.providers.get(provider_id)

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
            data[key] = self.get_provider(key).generate()

        return self.generate_items(**data)

    def generate_from_data(self, **data):
        new_data = {key: self.get_provider(key).by_value(value) for key, value in data.items()}
        return self.generate_items(**new_data)

    def generate_templates(self, **data):
        items = self.generate_from_data(**data)
        return {key: template.format(**items) for key, template in self.templates.items()}

    def generate(self, **data):
        templates = self.generate_templates(**data)
        return self.text.format(**templates)
